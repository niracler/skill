import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    module_path = REPO_ROOT / "scripts" / "quick_validate.py"
    spec = importlib.util.spec_from_file_location("quick_validate", module_path)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load quick_validate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_skill


class QuickValidateTest(unittest.TestCase):
    def test_accepts_folded_yaml_description(self) -> None:
        validate_skill = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir) / "sample-skill"
            skill_root.mkdir()
            (skill_root / "SKILL.md").write_text(
                """---
name: sample-skill
description: >-
  A folded description with multiple lines.
  It remains valid YAML frontmatter.
---

# Sample Skill
""",
                encoding="utf-8",
            )

            valid, message = validate_skill(skill_root)

        self.assertTrue(valid, message)


if __name__ == "__main__":
    unittest.main()
