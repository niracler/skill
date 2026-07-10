import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check-horizontal-rules.sh"


class HorizontalRuleCheckerTest(unittest.TestCase):
    def run_checker(self, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.md"
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [str(CHECKER), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_ignores_horizontal_rules_inside_fenced_code(self) -> None:
        result = self.run_checker(
            """# Example

```markdown
---
title: Embedded frontmatter
---
```
"""
        )

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_horizontal_rules_in_document_content(self) -> None:
        result = self.run_checker("# Example\n\n---\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("horizontal rule found", result.stdout)


if __name__ == "__main__":
    unittest.main()
