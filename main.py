import datetime as dt
import html as H
import json
import os
import re
import shutil
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from xml.sax.saxutils import escape as xml_escape

from psychology_engine import framework_summary, prompt_guidance

API = "https://api.github.com"
UA = {"User-Agent": "Omni-Hub/2.0"}
UTC = dt.timezone.utc

def now():
    return dt.datetime.now(UTC)

def log_activity(action, details):
    try:
        with open("ledger.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"timestamp": now().isoformat(), "action": action, "details": details}, ensure_ascii=False, default=str) + "\n")
    except OSError:
        print("WARN: activity ledger unavailable")

def atomic_text(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".omni-", dir=os.path.dirname(path) or ".", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)

def save_json(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        backup = path + ".corrupt-" + now().strftime("%Y%m%d%H%M%S")
        shutil.copy2(path, backup)
        log_activity("JSON_RECOVERY", {"path": path, "backup": backup, "error": str(exc)})
        return default

def strip_fences(value):
    value = (value or "").strip()
    value = re.sub(r"^\s*```(?:json)?\s*", "", value, flags=re.I)
    return re.sub(r"\s*```\s*$", "", value).strip()

def gh_get(url, retries=4):
    headers = {**UA, "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = exc.headers.get("Retry-After")
                time.sleep(int(wait) if wait and wait.isdigit() else min(60, 5 * 2**attempt))
                continue
            raise
        except (TimeoutError, urllib.error.URLError):
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)
    raise RuntimeError("GitHub retries exhausted")

def post_json(url, payload, headers=None):
    request = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={**UA, "Content-Type": "application/json", **(headers or {})}, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8", "replace")
        return response.status, json.loads(body) if body else {}

def normalize(item):
    pushed = item.get("pushed_at") or item.get("updated_at") or ""
    return {"name": item["full_name"], "url": item["html_url"], "desc": item.get("description") or "",
            "stars": int(item.get("stargazers_count", 0)), "pushed": pushed[:10]}

def validate_config(config):
    if not isinstance(config, dict) or not isinstance(config.get("settings"), dict):
        raise ValueError("config.json must contain settings")
    if not isinstance(config.get("categories"), list) or not config["categories"]:
        raise ValueError("config.json must contain categories")
    for category in config["categories"]:
        if not category.get("name") or not category.get("query"):
            raise ValueError("Each category needs name and query")
    config["per_category"] = max(1, min(20, int(config.get("per_category", 5))))
    config["settings"].setdefault("ai_model", "gemini-3.8-flash")
    config["settings"].setdefault("output_file", "README.md")
    return config

def search(query, count):
    since = (now() - dt.timedelta(days=365)).date()
    q = f"{query} stars:>30 fork:false archived:false pushed:>{since}"
    url = f"{API}/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page={min(100, count*4)}"
    return [normalize(x) for x in gh_get(url).get("items", [])]

def discover(config):
    seen, categories = set(), {}
    for category in config["categories"]:
        rows = []
        try:
            for item in search(category["query"], config["per_category"]):
                if item["url"] not in seen:
                    seen.add(item["url"])
                    rows.append(item)
                if len(rows) >= config["per_category"]:
                    break
            categories[category["name"]] = rows
            log_activity("CATEGORY_OK", {"name": category["name"], "count": len(rows)})
        except Exception as exc:
            categories[category["name"]] = []
            log_activity("CATEGORY_FAIL", {"name": category["name"], "error": str(exc)})
        time.sleep(1)
    rising = []
    rc = config.get("rising")
    if rc:
        try:
            day = (now() - dt.timedelta(days=max(1, int(rc.get("days", 30))))).date()
            q = f"{rc['query']} created:>{day} stars:>10 fork:false archived:false"
            url = f"{API}/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page=20"
            rising = [normalize(x) for x in gh_get(url).get("items", [])]
        except Exception as exc:
            log_activity("RISING_FAIL", str(exc))
    return categories, rising

def ai_text(config, repos, pick):
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        log_activity("AI_FALLBACK", "OPENROUTER_API_KEY absent; deterministic copy used")
        return {}
    prompt = f"""
You are an honest developer-resource curator. Use only the supplied repository names and
descriptions; never invent capabilities, metrics, urgency or scarcity.
Psychology guidance: {prompt_guidance()}
Repositories: {json.dumps([{'name': r['name'], 'desc': r['desc']} for r in repos], ensure_ascii=False)}
Pick: {pick['name']}
Return only JSON: intro (2-3 lines), quickstart (safe useful tip), pick_reason (one sentence),
descriptions (object keyed by exact repo name; each value max 14 words).
"""
    try:
        # openrouter/free selects only currently available free models.
        # Never add paid models to this request or its fallback list.
        _, result = post_json(
            "https://openrouter.ai/api/v1/chat/completions",
            {"model": "openrouter/free",
             "messages": [{"role": "user", "content": prompt}],
             "temperature": 0.2},
            {"Authorization": "Bearer " + key,
             "HTTP-Referer": "https://github.com/eshanmehra20-web/mr-sky-app",
             "X-Title": "Omni-Hub"})
        choices = result.get("choices") or []
        content = choices[0].get("message", {}).get("content") if choices else None
        if isinstance(content, list):
            content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
        data = json.loads(strip_fences(content if isinstance(content, str) else ""))
        if not isinstance(data, dict):
            raise ValueError("AI output must be a JSON object")
        valid_names = {r["name"] for r in repos}
        desc = data.get("descriptions", {})
        data["descriptions"] = {k: str(v)[:180] for k, v in desc.items()
                                if k in valid_names and isinstance(v, str)} if isinstance(desc, dict) else {}
        for k in ("intro", "quickstart", "pick_reason"):
            if k in data and not isinstance(data[k], str):
                data.pop(k)
        log_activity("OPENROUTER_OK", {"model": result.get("model", "openrouter/free")})
        return data
    except Exception as exc:
        log_activity("AI_FALLBACK", {"provider": "OpenRouter free router", "error": str(exc)})
        return {}

def safe_md(value, limit=140):
    return str(value or "").replace("|", "\\|").replace("\n", " ")[:limit]

def make_table(rows, descriptions):
    out = ["| Resource | Why it matters | ⭐ Stars | Updated |", "|---|---|---:|---|"]
    for r in rows:
        out.append(f"| [{r['name']}]({r['url']}) | {safe_md(descriptions.get(r['name']) or r['desc'])} | {r['stars']:,} | {r['pushed']} |")
    return out + [""]

def build_readme(cats, rising, new_items, ai, pick, repo, base, stamp):
    desc = ai.get("descriptions", {})
    all_rows = [r for rows in cats.values() for r in rows]
    top = sorted(all_rows, key=lambda r: r["stars"], reverse=True)[:3]
    out = ["# 🚀 Omni-Hub", ""]
    if repo:
        out += [f"![Stars](https://img.shields.io/github/stars/{repo}?style=flat-square) ![Updated](https://img.shields.io/github/last-commit/{repo}?label=auto-updated&style=flat-square)", ""]
    out += [ai.get("intro", "Discover useful open-source developer resources, refreshed automatically."),
            "", f"> **Live pulse:** {len(all_rows)} projects · {len(cats)} categories · checked {stamp}",
            "> **Ethical UX:** 4 psychology cycles · 120 principles · privacy-first"]
    if base:
        out.append(f"> 🔎 Searchable website: {base}")
    out += ["", "## ⚡ Start here", ""]
    out += [f"{i}. [{r['name']}]({r['url']}) — {safe_md(desc.get(r['name']) or r['desc'], 100)}"
            for i, r in enumerate(top, 1)]
    out.append("")
    if ai.get("quickstart"):
        fence = chr(96) * 3
        out += [fence + "bash", ai["quickstart"].strip(), fence, ""]
    out += [f"## 🎯 Pick of the day ({stamp[:10]})", "",
            f"**[{pick['name']}]({pick['url']})** ⭐ {pick['stars']:,} — {ai.get('pick_reason', safe_md(pick['desc']))}", ""]
    if new_items:
        out += ["## 🆕 New since last update", ""] + [f"- [{r['name']}]({r['url']}) ⭐ {r['stars']:,}" for r in new_items[:8]] + [""]
    if rising:
        out += ["## 📈 Rising this month", ""] + make_table(rising, desc)
    for name, rows in cats.items():
        if rows:
            out += [f"## {name}", ""] + make_table(rows, desc)
    out += ["---", "### How this page stays alive",
            "A scheduled workflow searches GitHub, filters archived/stale repositories, tracks new projects, "
            "and rebuilds this page. Rules are in config.json. AI copy is optional; discovery works without a Gemini key.", ""]
    if repo:
        out += [f"💡 [Suggest a project](https://github.com/{repo}/issues/new/choose) · Watch Releases for weekly digests.", ""]
    return "\n".join(out)

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Omni-Hub</title>
<meta name="description" content="__INTRO__"><meta property="og:title" content="Omni-Hub">
<meta property="og:description" content="__INTRO__"><link rel="canonical" href="__BASE__">
<link rel="alternate" type="application/atom+xml" href="feed.xml">
<style>:root{color-scheme:light dark;--bg:#fff;--fg:#18181b;--card:#f4f4f5;--mut:#666;--ac:#2563eb}
@media(prefers-color-scheme:dark){:root{--bg:#111;--fg:#eee;--card:#202024;--mut:#aaa;--ac:#93b4ff}}
*{box-sizing:border-box}body{margin:0;padding:18px;max-width:900px;margin-inline:auto;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui}
input{width:100%;padding:13px;border-radius:12px;border:1px solid var(--mut);background:var(--card);color:var(--fg)}
.card{display:block;padding:13px;margin:9px 0;border-radius:12px;background:var(--card);color:var(--fg);text-decoration:none}
.card:hover{outline:2px solid var(--ac)}.card b{color:var(--ac)}.card span,.card small{display:block}.card small{color:var(--mut)}</style>
</head><body><h1>🚀 Omni-Hub</h1><p>__INTRO__</p><p><small>Updated __DATE__ · automated daily refresh</small></p>
<label for="q">Search resources</label><input id="q" type="search" placeholder="Search projects…" autocomplete="off">
<div id="list" aria-live="polite"></div><script>
const D=__DATA__,el=document.getElementById('list'),q=document.getElementById('q');
function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function draw(){let t=q.value.toLowerCase(),h='';for(const [c,rows] of Object.entries(D.categories)){
let a=rows.filter(x=>(x.name+' '+x.desc).toLowerCase().includes(t));if(!a.length)continue;
h+='<h2>'+esc(c)+'</h2>'+a.map(x=>'<a class="card" target="_blank" rel="noopener noreferrer" href="'+esc(x.url)+'"><b>'+esc(x.name)+'</b><span>'+esc(x.desc)+'</span><small>⭐ '+Number(x.stars).toLocaleString()+' · '+esc(x.pushed)+'</small></a>').join('')}
el.innerHTML=h||'<p>No match.</p>'}q.addEventListener('input',draw);draw();</script></body></html>"""

def write_site(cats, rising, desc, ai, feed, base, stamp):
    os.makedirs("docs", exist_ok=True)
    groups = ({"📈 Rising this month": rising} if rising else {}) | cats
    data = {"updated": stamp, "psychology_framework": framework_summary(), "categories": {
        name: [{"name": r["name"], "url": r["url"], "desc": desc.get(r["name"]) or r["desc"],
                "stars": r["stars"], "pushed": r["pushed"]} for r in rows]
        for name, rows in groups.items()}}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    intro = H.escape(ai.get("intro", "Open-source developer resources, refreshed automatically."), quote=True)
    page = HTML.replace("__DATA__", blob).replace("__INTRO__", intro).replace("__BASE__", H.escape(base, quote=True)).replace("__DATE__", stamp[:10])
    atomic_text("docs/index.html", page)
    save_json("docs/data.json", data)
    lines = ["# Omni-Hub", "", f"> {ai.get('intro', 'Open-source developer resources.')}", "", "## Resources", ""]
    for name, rows in groups.items():
        lines.append(f"### {name}")
        lines += [f"- [{r['name']}]({r['url']}): {safe_md(desc.get(r['name']) or r['desc'])}" for r in rows]
    atomic_text("docs/llms.txt", "\n".join(lines) + "\n")
    entries = []
    for e in feed:
        date = e.get("date", stamp[:10])
        entries.append(f"<entry><title>{xml_escape(e['title'])}</title><id>{xml_escape(base)}#{date}</id>"
                       f"<updated>{date}T00:00:00Z</updated><link href=\"{xml_escape(base)}\"/>"
                       f"<summary>{xml_escape(e['summary'])}</summary></entry>")
    atom = ('<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom">'
            f"<title>Omni-Hub</title><id>{xml_escape(base or 'omni-hub')}</id><updated>{stamp}</updated>"
            f'<link href="{xml_escape(base)}"/><author><name>Omni-Hub bot</name></author>'
            + "".join(entries) + "</feed>")
    atomic_text("docs/feed.xml", atom)
    if base:
        atomic_text("docs/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n")
        atomic_text("docs/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                    f"<url><loc>{xml_escape(base)}</loc><lastmod>{stamp[:10]}</lastmod></url></urlset>")

def publish_extras(repo, base, new_items, pick, ai, all_rows, stamp):
    weekly = now().weekday() == 0 or os.getenv("FORCE_WEEKLY") == "1"
    rows = new_items[:8] or sorted(all_rows, key=lambda r: -r["stars"])[:5]
    body = "## " + ("New this week" if new_items else "Top picks") + "\n\n"
    body += "\n".join(f"- [{r['name']}]({r['url']}) ⭐ {r['stars']:,}" for r in rows)
    body += f"\n\nFull list: {base or ('https://github.com/' + repo)}\n"
    token = os.getenv("GITHUB_TOKEN")
    if weekly and repo and token:
        tag = "digest-" + stamp[:10]
        try:
            gh_get(f"{API}/repos/{repo}/releases/tags/{tag}")
            log_activity("RELEASE_SKIP_DUPLICATE", tag)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                try:
                    post_json(f"{API}/repos/{repo}/releases",
                              {"tag_name": tag, "name": f"Weekly digest {stamp[:10]}", "body": body},
                              {"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json"})
                    log_activity("RELEASE_OK", tag)
                except Exception as err:
                    log_activity("RELEASE_FAIL", str(err))
            else:
                log_activity("RELEASE_CHECK_FAIL", str(exc))
    tg, chat = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if tg and chat:
        try:
            post_json(f"https://api.telegram.org/bot{tg}/sendMessage",
                      {"chat_id": chat, "text": f"🎯 {pick['name']}\n{pick['url']}\n{ai.get('pick_reason','')}\n{base}"})
            log_activity("TELEGRAM_OK", stamp[:10])
        except Exception as exc:
            log_activity("TELEGRAM_FAIL", str(exc))
    dev = os.getenv("DEVTO_API_KEY")
    if weekly and dev:
        try:
            post_json("https://dev.to/api/articles", {"article": {
                "title": f"Top GitHub resources this week ({stamp[:10]})", "body_markdown": body,
                "published": os.getenv("DEVTO_PUBLISH") == "1",
                "tags": ["github", "opensource", "programming", "webdev"], "canonical_url": base or None}},
                {"api-key": dev})
            log_activity("DEVTO_OK", stamp[:10])
        except Exception as exc:
            log_activity("DEVTO_FAIL", str(exc))

def main():
    stamp = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    config = validate_config(load_json("config.json", {}))
    out_file = config["settings"]["output_file"]
    repo = os.getenv("GITHUB_REPOSITORY", "")
    parts = repo.split("/", 1)
    base = f"https://{parts[0]}.github.io/{parts[1]}/" if len(parts) == 2 else ""
    try:
        cats, rising = discover(config)
        all_rows = [r for rows in cats.values() for r in rows]
        if len(all_rows) < 5:
            raise RuntimeError(f"Only {len(all_rows)} projects found; published files preserved")
        state = load_json("state.json", {"urls": [], "feed": []}) or {"urls": [], "feed": []}
        known = set(state.get("urls", []))
        pool = all_rows + [r for r in rising if r["url"] not in {x["url"] for x in all_rows}]
        new_items = [r for r in pool if r["url"] not in known] if known else []
        pick = sorted(pool, key=lambda r: (r["stars"], r["name"]), reverse=True)[int(now().strftime("%j")) % len(pool)]
        ai = ai_text(config, pool, pick)
        if os.path.exists(out_file):
            shutil.copy2(out_file, out_file + ".bak")
        atomic_text(out_file, build_readme(cats, rising, new_items, ai, pick, repo, base, stamp))
        entry = {"date": stamp[:10], "title": f"{len(new_items)} new projects" if new_items else f"Pick: {pick['name']}",
                 "summary": ", ".join(r["name"] for r in new_items[:8]) or ai.get("pick_reason", pick["url"])}
        feed = ([entry] + [e for e in state.get("feed", []) if e.get("date") != stamp[:10]])[:20]
        write_site(cats, rising, ai.get("descriptions", {}), ai, feed, base, stamp)
        save_json("state.json", {"urls": sorted({r["url"] for r in pool}), "feed": feed})
        publish_extras(repo, base, new_items, pick, ai, all_rows, stamp)
        log_activity("OMNI_HUB_SYNC", {"projects": len(all_rows), "rising": len(rising), "new": len(new_items)})
        print(f"Done: {len(all_rows)} projects, {len(new_items)} new.")
    except Exception as exc:
        log_activity("OMNI_HUB_ERROR", str(exc))
        raise

if __name__ == "__main__":
    main()
