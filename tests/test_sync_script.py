import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync"


class SyncScriptTest(unittest.TestCase):
    def make_repo(self, root: Path, skills: list[tuple[str, str]]) -> Path:
        script_path = root / "scripts" / "sync"
        script_path.parent.mkdir(parents=True)
        shutil.copy2(SYNC_SCRIPT, script_path)
        script_path.chmod(0o755)
        for plugin_name, skill_name in skills:
            skill_root = root / "plugins" / plugin_name / "skills" / skill_name
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                f"---\nname: {skill_name}\ndescription: Test skill.\n---\n",
                encoding="utf-8",
            )
        return script_path

    def run_sync(self, script_path: Path) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(script_path.parents[1] / "home")
        return subprocess.run(
            [str(script_path), "--dry-run"],
            cwd=script_path.parents[1],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_discovers_skills_inside_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = self.make_repo(
                Path(temp_dir), [("developer", "alpha"), ("personal", "beta")]
            )

            result = self.run_sync(script_path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("alpha", result.stdout)
        self.assertIn("beta", result.stdout)
        self.assertIn("预览完成 (2/2)", result.stdout)

    def test_rejects_duplicate_skill_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = self.make_repo(
                Path(temp_dir), [("first", "shared"), ("second", "shared")]
            )

            result = self.run_sync(script_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("重复的 skill 名称: shared", result.stderr)


if __name__ == "__main__":
    unittest.main()
