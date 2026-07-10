import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def marketplace_entry(name: str, path: str) -> dict[str, object]:
    return {
        "name": name,
        "source": {"source": "local", "path": path},
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Developer Tools",
    }


def write_plugin(root: Path, name: str, skill_name: str | None = None) -> None:
    write_json(
        root / "plugins" / name / ".codex-plugin" / "plugin.json",
        {
            "name": name,
            "version": "0.1.0",
            "description": "Test plugin",
            "author": {"name": "Test author"},
            "skills": "./skills/",
            "interface": {
                "displayName": "Test Plugin",
                "shortDescription": "Test plugin",
                "longDescription": "Test plugin for validation.",
                "developerName": "Test author",
                "category": "Developer Tools",
                "capabilities": [],
                "defaultPrompt": ["Test the plugin."],
            },
        },
    )
    resolved_skill = skill_name or name
    skill_root = root / "plugins" / name / "skills" / resolved_skill
    skill_root.mkdir(parents=True, exist_ok=True)
    (skill_root / "SKILL.md").write_text(
        f"---\nname: {resolved_skill}\ndescription: Test skill.\n---\n",
        encoding="utf-8",
    )


class ValidatePluginsTest(unittest.TestCase):
    def load_validator(self):
        module_path = REPO_ROOT / "scripts" / "validate_plugins.py"
        self.assertTrue(module_path.is_file(), "scripts/validate_plugins.py is missing")
        spec = importlib.util.spec_from_file_location("validate_plugins", module_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec else None)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module.validate_repository

    def test_rejects_duplicate_plugin_ids(self) -> None:
        validate_repository = self.load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_json(
                root / ".agents" / "plugins" / "marketplace.json",
                {
                    "name": "test-marketplace",
                    "plugins": [
                        marketplace_entry("sample", "./plugins/sample"),
                        marketplace_entry("sample", "./plugins/other"),
                    ],
                },
            )
            errors = validate_repository(root)

        self.assertTrue(any("duplicate plugin name `sample`" in e for e in errors))

    def test_rejects_paths_outside_plugins_directory(self) -> None:
        validate_repository = self.load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_json(
                root / ".agents" / "plugins" / "marketplace.json",
                {
                    "name": "test-marketplace",
                    "plugins": [marketplace_entry("sample", "./sample")],
                },
            )
            errors = validate_repository(root)

        self.assertTrue(any("must stay under `./plugins/`" in e for e in errors))

    def test_rejects_missing_manifest_and_invalid_semver(self) -> None:
        validate_repository = self.load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_json(
                root / ".agents" / "plugins" / "marketplace.json",
                {
                    "name": "test-marketplace",
                    "plugins": [
                        marketplace_entry("missing", "./plugins/missing"),
                        marketplace_entry("sample", "./plugins/sample"),
                    ],
                },
            )
            write_plugin(root, "sample")
            manifest_path = root / "plugins/sample/.codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["version"] = "dev"
            write_json(manifest_path, manifest)
            errors = validate_repository(root)

        self.assertTrue(any("plugin directory is missing" in e for e in errors))
        self.assertTrue(any("version must use strict SemVer" in e for e in errors))

    def test_rejects_duplicate_skill_names_across_plugins(self) -> None:
        validate_repository = self.load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_json(
                root / ".agents" / "plugins" / "marketplace.json",
                {
                    "name": "test-marketplace",
                    "plugins": [
                        marketplace_entry("first", "./plugins/first"),
                        marketplace_entry("second", "./plugins/second"),
                    ],
                },
            )
            write_plugin(root, "first", "shared-skill")
            write_plugin(root, "second", "shared-skill")
            errors = validate_repository(root)

        self.assertTrue(any("duplicate skill name `shared-skill`" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
