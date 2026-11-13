# Mr. Sky / Omni-Hub — Master Blueprint 300x
**Status:** Architecture and implementation plan  
**Version:** 1.0  
**Principle:** Additive-only. Preserve all existing files, features, history, and working behavior.

## 0. Non-negotiable project rules
1. Never delete existing project files, code, features, branches, backups, or history as part of this upgrade.
2. Do not overwrite existing behavior until the replacement is tested and a rollback path exists.
3. Make changes on a feature branch, run tests, review the diff, and use a pull request before merging to `main`.
4. Keep secrets out of source code. Use GitHub Actions Secrets or a server-side secret store.
5. Free-first: use free tiers and open-source tools. No paid service, subscription, hosting, API credit, or domain purchase without explicit owner approval.
6. Never claim a feature is live until it has been deployed and verified.
7. Treat “300x” as a quality, reliability, usefulness, and growth ambition—not a measurable or guaranteed 300-fold performance claim.
8. Build ethically: no fake traffic, fake reviews, fabricated testimonials, dark patterns, coercive upsells, or misleading scarcity.

## 1. Product and business direction
**Business model:** Hybrid — Free + Premium + Business + API.  
**Priority:** Useful product → customers → sustainable revenue.

The first goal is a useful, trustworthy product. Customer acquisition follows demonstrated value. Monetization follows repeatable value and transparent pricing. Any example prices are placeholders until separately approved.

## 2. Three-layer / two-account architecture
The intended architecture has two GitHub accounts and three repositories/layers:

### Layer A — Public Customer Platform
- Lives in the second GitHub account; account and repository names are intentionally unspecified until supplied by the owner.
- Holds customer-facing website/UI, public documentation, onboarding, help pages, and non-sensitive client code.
- Must not contain private engine source, credentials, internal prompts, private datasets, or privileged tokens.

### Layer B — Public Mr. Sky / Omni-Hub
- Existing repository: `eshanmehra20-web/mr-sky-app`.
- Preserve its existing Omni-Hub discovery engine, Pages site, automation, workflows, tests, and `advait_core.py`.
- Public repository code is copyable. Choose and document a suitable license; do not assume public code can be made secret.
- Do not put private master-engine logic or secrets here.

### Layer C — Private Master Core Engine
- A separate private repository under the owner's GitHub account, to be created only after its name and setup are approved.
- Holds sensitive orchestration, proprietary logic, server-side tools, private prompts/configuration, and internal service code.
- Secrets belong in GitHub Secrets or a secure runtime secret store, never committed files.
- Public layers call it through a narrow authenticated API. Validate inputs, authenticate callers, rate-limit, log safely, and return only permitted outputs.

### Security controls
- Enable 2FA on both accounts; use unique passwords and recovery methods.
- Apply least-privilege tokens, short scopes, rotation, and separate credentials per environment.
- Protect `main`, require CI checks where available, review dependency changes, and keep backups.
- Never connect a public-repository workflow to private infrastructure using an exposed self-hosted runner.
- A private repository alone does not provide a running API server.

## 3. Existing system — preserve and extend
Known existing components in `mr-sky-app` include:
- `advait_core.py` (existing core; preserve and assess separately before integration).
- `main.py` and `config.json`.
- OpenRouter integration using `OPENROUTER_API_KEY` from GitHub Secrets and the `openrouter/free` route.
- GitHub repository discovery, categories, ranking, descriptions, README generation, state and activity ledger.
- GitHub Pages searchable site and generated feeds/metadata.
- GitHub Actions workflow, tests, backups/recovery and safe fallbacks.
- Telegram/Dev.to integrations where configured.

Important current limitations to plan for:
- OpenRouter free routing is not yet a complete independent multi-provider failover system.
- `advait_core.py` is not assumed to be integrated into the Omni-Hub workflow.
- Voice assistant is a desired capability, not an already verified website feature.
- GitHub Actions runs jobs; it is not a persistent 24/7 backend.
- GitHub Pages is static hosting; it cannot itself run private server-side engine code.
- The second GitHub account and its customer-platform repository are not yet identified.

## 4. Implementation sequence and release gates
### Phase 0 — Inventory and baseline
- Record current default branch, commit SHA, files, workflow status, Pages URL, secrets names (never values), and test results.
- Preserve a dated baseline and existing backup branch.
- Map every planned feature to an existing file or a new file.
- Do not delete, rename, or replace anything during inventory.

### Phase 1 — Product clarity and customer value
- Define the first target users and their real problems.
- Choose a small set of useful first workflows and define success measures.
- Make the landing page accurately describe the actual product.
- Add clear onboarding, examples, help, privacy notice, and feedback path.

### Phase 2 — Ethical psychology framework
- Apply the 120 principles in Section 5 in the order: Need → Human → Robotic → Money.
- Treat them as design hypotheses to test, not as universal facts about every person.
- Respect user choice, accessibility, consent, and privacy.

### Phase 3 — Measurement and privacy
- Add a privacy-respecting website analytics provider only after its site/account identifier and privacy settings are configured.
- Separate public website visits from Git clone counts and from the project's own automation.
- Validate that the analytics script fires on the published Pages site.
- Do not infer a visitor's identity. Avoid collecting names, email addresses, precise location, or sensitive attributes.
- Establish a baseline before interpreting growth.

### Phase 4 — Growth and content
- Improve page titles, descriptions, canonical URL, Open Graph preview, semantic headings, internal links, sitemap, and useful content.
- Publish genuinely useful examples, tutorials, release notes, and feature updates.
- Make sharing and project suggestions easy without spam or deceptive prompts.
- Use search intent and real user feedback to prioritize content.

### Phase 5 — Engine reliability
- Add provider adapters behind a common interface.
- Use free providers first, with explicit quotas, timeouts, retries, circuit breakers, and deterministic fallback.
- Track provider health without logging prompts or secrets unnecessarily.
- Add model quality checks and task-based routing; do not silently switch to a paid provider.
- Keep OpenRouter as the current configured route until another provider is tested.

### Phase 6 — Voice assistant
- Add speech input and speech output as separate, testable modules.
- Provide a text fallback, permission prompts, clear recording controls, and error states.
- Disclose when speech is sent to a remote provider and avoid recording without user action.
- Keep voice costs at zero unless the owner approves otherwise.

### Phase 7 — Private Core API
- Create the private repository only after account/repo name confirmation.
- Design a minimal authenticated API, request schema validation, quotas, audit logging, and safe error responses.
- Keep all privileged keys and private logic server-side.
- Choose a runtime only after comparing truly free limits and uptime constraints. Do not promise 24/7 availability from scheduled Actions or static Pages.

### Phase 8 — Business readiness
- Keep Free usable and explain limits transparently.
- Introduce Premium/Business/API only after product value and support needs are validated.
- Add payment gateway only after owner approval and after checking current fees, eligibility, and legal requirements.
- Never store card data directly; use a reputable hosted payment flow.

### Phase 9 — Verification and release
- Run syntax checks, unit tests, integration tests, security checks, accessibility checks, and a manual mobile test.
- Review all changed files and confirm no deletions.
- Deploy from a reviewed pull request.
- Verify the public site, analytics events, links, workflows, and rollback path.
- Publish a concise release note with known limitations.

## 5. Psychology framework — 120 principles
These are ethical product-design prompts. Use them to reduce friction and improve usefulness; never to exploit vulnerabilities.

### A. Need Psychology — 30
1. Identify the user's actual job-to-be-done.
2. Ask what problem occurs most frequently.
3. Distinguish urgent needs from optional wishes.
4. Identify the current workaround.
5. Understand the cost of the current workaround in time and effort.
6. Start with one clear use case.
7. Explain the outcome before listing features.
8. Match feature complexity to user skill.
9. Offer a beginner path and an advanced path.
10. Make the first useful result quick to reach.
11. Provide examples based on real tasks.
12. Show prerequisites before a workflow begins.
13. Make limitations visible before the user invests effort.
14. Support the user's language where feasible.
15. Design for mobile-first use.
16. Make error recovery understandable.
17. Provide a useful alternative when a feature is unavailable.
18. Let users save or export their work.
19. Make recurring tasks easier without forcing automation.
20. Provide clear help at the point of need.
21. Collect feedback about unmet needs.
22. Group related needs into understandable workflows.
23. Prioritize frequent, high-impact problems.
24. Validate assumptions with real usage data.
25. Do not build features solely because competitors have them.
26. Explain who a feature is for and who it is not for.
27. Make accessibility a core need, not an afterthought.
28. Provide predictable performance and status messages.
29. Close the loop when a user reports a problem.
30. Revisit priorities as evidence changes.

### B. Human Psychology — 30
1. Reduce cognitive load.
2. Use plain, familiar language.
3. Keep the primary action obvious.
4. Break long tasks into manageable steps.
5. Show progress during multi-step work.
6. Provide a quick, honest first success.
7. Keep navigation predictable.
8. Use consistent labels and visual patterns.
9. Offer user control over optional features.
10. Explain why a permission is needed.
11. Ask for the minimum information necessary.
12. Make undo or recovery possible where practical.
13. Use helpful defaults that can be changed.
14. Make empty states instructive.
15. Use real examples instead of vague claims.
16. Make feedback specific and actionable.
17. Respect different levels of technical knowledge.
18. Avoid shame, blame, or condescending copy.
19. Use social proof only when authentic and verifiable.
20. Clearly distinguish facts, estimates, and suggestions.
21. Avoid fake urgency and artificial scarcity.
22. Make privacy choices understandable.
23. Support keyboard and assistive-technology navigation.
24. Use readable contrast and typography.
25. Avoid surprise changes to user data.
26. Explain automated actions before they happen.
27. Let users choose notification frequency.
28. Acknowledge errors honestly and explain next steps.
29. Build trust through consistent behavior.
30. Test usability with real people and revise from evidence.

### C. Robotic Psychology — 30
Here “Robotic Psychology” means the AI assistant's interaction and reliability design, not a claim that software has human feelings.
1. Identify itself as an AI assistant.
2. State capabilities and limitations accurately.
3. Ask clarifying questions only when necessary.
4. Keep responses relevant to the user's task.
5. Follow a stable interaction style.
6. Separate known facts from inferences.
7. Cite or expose sources for factual claims when available.
8. Admit uncertainty instead of fabricating.
9. Never claim an action succeeded before verification.
10. Confirm consequential actions before execution.
11. Respect user permissions and access boundaries.
12. Never expose secrets or private system prompts.
13. Validate tool inputs before execution.
14. Use least-privilege tools.
15. Handle tool failures with safe fallbacks.
16. Avoid repeating a failed action indefinitely.
17. Keep an auditable record of important actions.
18. Minimize sensitive data in logs.
19. Preserve context only according to clear privacy rules.
20. Let users correct misunderstandings.
21. Distinguish generated suggestions from executed changes.
22. Provide progress for long-running tasks.
23. Use deterministic behavior for safety-critical steps.
24. Route tasks to suitable models/tools based on capability.
25. Check outputs for format and schema validity.
26. Respect rate limits and provider terms.
27. Never silently incur paid API usage.
28. Make automation opt-in and controllable.
29. Provide human handoff or manual alternatives.
30. Evaluate reliability with repeatable tests.

### D. Money Psychology — 30
1. Explain the value before presenting a price.
2. Keep the Free plan genuinely useful.
3. State plan limits clearly.
4. Avoid hidden fees.
5. Show billing frequency and currency.
6. Distinguish one-time and recurring charges.
7. Explain cancellation and renewal terms.
8. Avoid preselected paid add-ons.
9. Never use deceptive countdowns.
10. Never fabricate discounts or reference prices.
11. Make plan comparisons easy to understand.
12. Match pricing to real usage and operating costs.
13. Validate willingness to pay with user research.
14. Offer a low-risk way to try the product.
15. Explain what happens when a quota is reached.
16. Warn before any paid overage.
17. Require explicit consent before paid usage.
18. Provide receipts and transparent payment status.
19. Use hosted payment providers; do not store card details.
20. Explain refund and support policies.
21. Make Free-to-Premium upgrades optional.
22. Do not degrade Free features to force upgrades.
23. Offer Business plans only when business needs are served.
24. Publish API rate limits and pricing clearly.
25. Show usage and remaining quota.
26. Protect users from accidental duplicate purchases.
27. Keep taxes and transaction fees transparent.
28. Measure retention and satisfaction, not only conversion.
29. Avoid exploiting financial stress or urgency.
30. Review pricing when costs or product value change.

## 6. Smart Growth Tracker and Analytics
### Goals
- Count page views and unique visitors using an approved privacy-friendly analytics provider.
- Identify top pages, referrer categories, broad device classes, and trends where supported.
- Measure meaningful events such as search use, project-link clicks, feedback submissions, and sign-up intent only when appropriate.
- Separate website analytics from GitHub repository traffic metrics.

### Data definitions
- Page view: a page load recorded by the analytics provider.
- Unique visitor: provider-defined approximate unique browser/device, not a verified human identity.
- Returning visitor: provider-defined repeat browser/device.
- Git clone: a repository clone event, not necessarily a website visit or a distinct customer.
- Conversion: a clearly defined voluntary action, not merely a page view.

### Privacy and quality
- Prefer aggregate, privacy-respecting analytics and minimal retention.
- Do not fingerprint visitors or attempt to identify named individuals.
- Do not collect sensitive personal data.
- Disclose analytics in a short privacy notice and respect applicable consent requirements.
- Filter or label internal tests and known automation where the provider supports it; never assume GitHub Actions explains all clones.
- Test events on the live Pages URL and record the verification date.

### Provider integration gate
No tracker is considered installed until:
1. The owner chooses/creates the analytics property.
2. A site identifier or approved script is obtained.
3. The script is added to the actual published HTML template.
4. The live site is checked and a test visit appears in the dashboard.
5. Privacy notice and consent requirements are reviewed.

A static GitHub Pages site cannot receive server-side events by itself. Do not add a made-up ID or claim tracking is active without a verified provider setup.

## 7. Growth Intelligence loop
1. Measure baseline.
2. Find the largest user friction point.
3. Form one specific improvement hypothesis.
4. Make one small additive change.
5. Test accessibility, speed, correctness, and privacy.
6. Compare results over a meaningful time window.
7. Keep, revise, or roll back based on evidence.
8. Publish a short change note.
9. Repeat; do not optimize for vanity metrics alone.

## 8. Metrics dashboard
Track only metrics that can be defined and verified:
- Website: page views, unique visitors, returning visitors, referrer groups, top pages.
- Engagement: searches, useful outbound clicks, feedback completion, repeat use.
- Product quality: task success, error rate, latency, availability, accessibility defects.
- AI engine: provider success rate, fallback rate, response validity, cost (must remain zero unless approved).
- Business: voluntary upgrade interest, paid conversion, retention, support burden—only after real product and payment flows exist.

## 9. Current decisions and pending owner inputs
- Confirm the second GitHub account and customer-platform repository name.
- Confirm whether/when to create the private Master Core repository.
- Select the analytics provider and create its site/property identifier.
- Confirm the privacy notice and any consent behavior before enabling analytics.
- Confirm any payment provider only after checking fees and terms.
- Confirm runtime/hosting only after free-tier and uptime limits are documented.

## 10. Definition of done
A phase is complete only when its code/documentation exists, tests pass, deployment is verified where relevant, privacy/security checks are complete, and the owner can inspect the result. A written plan is not a deployed feature. A deployment is not proof of visitors. A visitor count is not proof of customers.

---
**Preservation statement:** This blueprint is additive documentation. It does not authorize deleting or replacing existing repository files, the existing `advait_core.py`, existing automation, or prior backups.
