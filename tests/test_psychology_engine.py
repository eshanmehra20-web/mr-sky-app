import unittest

from psychology_engine import (
    framework_summary,
    get_all_principles,
    get_cycle,
    prompt_guidance,
    select_principles,
)


class PsychologyEngineTests(unittest.TestCase):
    def test_exactly_120_principles_in_four_cycles(self):
        all_items = get_all_principles()
        self.assertEqual(len(all_items), 120)
        self.assertEqual(len({item["id"] for item in all_items}), 120)
        for cycle in ("need", "human", "robotic", "money"):
            self.assertEqual(len(get_cycle(cycle)), 30)

    def test_cycle_order_and_summary(self):
        summary = framework_summary()
        self.assertEqual(summary["order"], ["need", "human", "robotic", "money"])
        self.assertEqual(summary["total_principles"], 120)
        self.assertEqual(summary["implementation_status"], "active_guidance_layer")

    def test_selector_is_bounded(self):
        self.assertEqual(len(select_principles("human", 5)), 5)
        self.assertEqual(len(select_principles("money", 0)), 0)
        with self.assertRaises(ValueError):
            select_principles("unknown")

    def test_prompt_contains_ethics_and_cost_guardrails(self):
        guidance = prompt_guidance().lower()
        self.assertIn("never manipulate", guidance)
        self.assertIn("no fake urgency", guidance)
        self.assertIn("paid", guidance)


if __name__ == "__main__":
    unittest.main()
