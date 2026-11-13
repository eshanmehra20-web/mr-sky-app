"""Ethical, privacy-first psychology guidance for the Omni-Hub experience.

This module contains 120 product-design principles in four agreed cycles.
It does not profile people, infer sensitive traits, or use coercive patterns.
"""
from __future__ import annotations

from typing import Any

_CYCLES = {
    "need": [
        "Identify the user's stated task before recommending anything.",
        "Put the most directly useful answer or resource first.",
        "Separate essential features from optional extras.",
        "Explain what problem each feature solves.",
        "Make the first useful action easy to find.",
        "Avoid adding steps that do not help complete the task.",
        "Offer a clear path when the requested item is unavailable.",
        "Show prerequisites before the user invests effort.",
        "Use plain language for needs and outcomes.",
        "Distinguish urgent user needs from promotional priorities.",
        "Let users compare relevant alternatives.",
        "Explain limitations before the user depends on a feature.",
        "Keep search results aligned with the entered query.",
        "Provide useful empty states and recovery suggestions.",
        "Preserve the user's progress when a task is interrupted.",
        "Make important actions discoverable without pressure.",
        "Ask only for information needed for the current task.",
        "Support different levels of experience with clear guidance.",
        "Show expected time or effort only when it is grounded.",
        "Make the next step explicit after each completed task.",
        "Do not manufacture a need to sell an unrelated feature.",
        "Allow users to defer nonessential setup.",
        "Explain who a feature is for and who may not need it.",
        "Prioritize reliability for repeated user needs.",
        "Provide a route to human support or documentation where possible.",
        "Keep task language consistent across the product.",
        "Make cancellation and exit paths easy to locate.",
        "Do not hide important conditions behind vague labels.",
        "Use feedback to fix recurring unmet needs, not to pressure users.",
        "Measure task success, not clicks alone."
    ],
    "human": [
        "Use respectful, calm, non-judgmental language.",
        "Make text readable on small screens.",
        "Provide accessible labels and keyboard navigation.",
        "Respect different abilities and interaction styles.",
        "Explain errors in a way that helps users recover.",
        "Never shame users for mistakes or lack of knowledge.",
        "Give users control over notifications.",
        "Avoid dark patterns, guilt, and emotional coercion.",
        "Use examples that clarify without stereotyping.",
        "Respect the user's time and attention.",
        "Make privacy choices understandable.",
        "Ask permission before optional data collection.",
        "Do not infer sensitive personal traits.",
        "Avoid fake testimonials, reviews, or popularity claims.",
        "Use honest language about AI-generated content.",
        "Provide confirmation for consequential actions.",
        "Allow users to review before submitting or paying.",
        "Keep support and contact routes visible.",
        "Use inclusive language and localization where feasible.",
        "Do not exploit fear, loneliness, or insecurity.",
        "Make it easy to correct personal input.",
        "Explain why a permission is requested.",
        "Keep consent separate from unrelated choices.",
        "Avoid distracting motion and unnecessary interruptions.",
        "Make destructive actions reversible where practical.",
        "Provide clear status during waiting or processing.",
        "Treat user feedback as voluntary and confidential.",
        "Avoid assuming a user's intent from a single action.",
        "Offer help without blocking independent choice.",
        "Design for trust through consistency and honesty."
    ],
    "robotic": [
        "Use deterministic rules for safety-critical product decisions.",
        "Validate inputs before processing them.",
        "Return structured outputs with documented fields.",
        "Keep automation steps observable through safe logs.",
        "Use retries with bounded backoff for transient failures.",
        "Make repeated operations idempotent where possible.",
        "Preserve existing data before changing generated files.",
        "Fail safely when a provider or dependency is unavailable.",
        "Keep secrets out of source code and logs.",
        "Separate public interfaces from private implementation.",
        "Use least-privilege permissions for integrations.",
        "Test normal, boundary, and failure cases.",
        "Record provenance for generated recommendations.",
        "Label estimates and uncertain results clearly.",
        "Do not claim a task succeeded before verification.",
        "Keep human approval for consequential external actions.",
        "Provide a manual fallback when automation fails.",
        "Version schemas and handle older stored data safely.",
        "Avoid hidden background actions that surprise users.",
        "Expose system status without leaking internal secrets.",
        "Use rate limits and resource budgets.",
        "Check external content as untrusted input.",
        "Keep provider selection transparent and cost-aware.",
        "Do not silently switch to paid services.",
        "Monitor error rates and recovery outcomes.",
        "Keep automated changes reviewable and reversible.",
        "Use accessibility and privacy checks in release tests.",
        "Minimize data retention and collection.",
        "Document what automation can and cannot do.",
        "Require explicit consent for high-impact actions."
    ],
    "money": [
        "Show the price and billing interval before commitment.",
        "Clearly distinguish free, trial, and paid features.",
        "Disclose taxes, fees, and usage limits where known.",
        "Never label a paid feature as free.",
        "Do not use fake discounts or inflated reference prices.",
        "Avoid fake countdowns and manufactured scarcity.",
        "Explain cancellation and refund terms before purchase.",
        "Do not preselect paid add-ons.",
        "Require clear confirmation before charging.",
        "Show usage and remaining quota where available.",
        "Warn before a user crosses a paid usage boundary.",
        "Offer a useful free path without deceptive degradation.",
        "Do not silently upgrade a plan.",
        "Explain what a plan includes and excludes.",
        "Make renewal timing and amount clear.",
        "Provide receipts and transaction status.",
        "Keep payment credentials with trusted payment providers.",
        "Never log card data, passwords, or payment secrets.",
        "Separate business value from pressure-based selling.",
        "Recommend a paid plan only when its benefits fit the stated need.",
        "Make downgrade and cancellation paths straightforward.",
        "Disclose API costs and rate limits to developers.",
        "Use transparent commission or affiliate disclosures.",
        "Do not fabricate earnings, savings, or ROI claims.",
        "Compare total costs using equivalent assumptions.",
        "Provide spending controls for metered services.",
        "Keep free-first defaults when they meet the task.",
        "Ask approval before enabling any paid provider.",
        "Make billing support easy to reach.",
        "Measure sustainable value and retention, not forced conversion."
    ],
}

_CYCLE_TITLES = {
    "need": "Need Psychology",
    "human": "Human Psychology",
    "robotic": "Robotic Psychology",
    "money": "Money Psychology",
}
_ORDER = ("need", "human", "robotic", "money")


def get_all_principles() -> list[dict[str, Any]]:
    """Return a fresh, ordered list of all 120 principles."""
    return [
        {"id": f"{cycle}-{index:02d}", "cycle": cycle,
         "title": _CYCLE_TITLES[cycle], "principle": principle}
        for cycle in _ORDER
        for index, principle in enumerate(_CYCLES[cycle], 1)
    ]


def get_cycle(cycle: str) -> list[dict[str, Any]]:
    """Return principles for one cycle; unknown names raise ValueError."""
    key = str(cycle).strip().lower().replace(" ", "_")
    if key not in _CYCLES:
        raise ValueError(f"Unknown psychology cycle: {cycle}")
    return [item for item in get_all_principles() if item["cycle"] == key]


def framework_summary() -> dict[str, Any]:
    """Small public-safe summary suitable for generated site metadata."""
    return {
        "version": 1,
        "order": list(_ORDER),
        "cycles": {
            key: {"title": _CYCLE_TITLES[key], "principle_count": len(_CYCLES[key])}
            for key in _ORDER
        },
        "total_principles": sum(len(_CYCLES[key]) for key in _ORDER),
        "guardrails": [
            "ethical UX only",
            "no sensitive-trait profiling",
            "no fake scarcity or social proof",
            "no coercive upselling",
            "no paid service without explicit approval",
            "privacy-first and data-minimizing"
        ],
        "implementation_status": "active_guidance_layer",
    }


def prompt_guidance() -> str:
    """Build explicit guardrails for optional AI copy generation."""
    lines = [
        "Apply these four ethical product-design cycles; never manipulate users.",
        "NEED: answer the stated task, reduce friction, explain limitations.",
        "HUMAN: be respectful, accessible, privacy-preserving and non-coercive.",
        "ROBOTIC: be accurate, testable, transparent, secure and cost-aware.",
        "MONEY: disclose real prices and limits; no fake urgency or hidden upsells; never enable paid services without approval.",
        "Never infer sensitive traits, invent proof, or claim unverified outcomes.",
    ]
    return "\n".join(lines)


def select_principles(cycle: str, limit: int | None = None) -> list[dict[str, Any]]:
    """Return a bounded subset for a UI surface or review screen."""
    items = get_cycle(cycle)
    if limit is None:
        return items
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return items[:limit]
