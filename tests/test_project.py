import ast
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class ProjectIntegrityTests(unittest.TestCase):
    def test_main_is_valid_python_syntax(self):
        ast.parse((ROOT / "main.py").read_text(encoding="utf-8"))

    def test_config_is_valid_and_has_all_eight_categories(self):
        config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
        self.assertEqual(len(config["categories"]), 8)
        self.assertEqual(config["settings"]["output_file"], "README.md")
        self.assertEqual(config["settings"]["ai_model"], "gemini-3.8-flash")

    def test_required_automation_files_exist(self):
        self.assertTrue((ROOT / ".github/workflows/omni-hub.yml").is_file())
        self.assertTrue((ROOT / ".github/ISSUE_TEMPLATE/suggest.yml").is_file())
        self.assertTrue((ROOT / "requirements.txt").is_file())

    def test_original_advait_core_is_preserved(self):
        self.assertTrue((ROOT / "advait_core.py").is_file())

if __name__ == "__main__":
    unittest.main()
