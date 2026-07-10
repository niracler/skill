import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

EXPECTED_PLUGINS = {
    "developer-workflows": {
        "category": "Developer Tools",
        "skills": {
            "workspace-init",
            "workspace-planning",
            "git-workflow",
            "code-sync",
            "ha-integration-reviewer",
            "markdown-lint",
            "skill-reviewer",
            "weekly-report",
            "yunxiao",
        },
    },
    "personal-knowledge": {
        "category": "Knowledge & Files",
        "skills": {
            "schedule-manager",
            "pinboard-manager",
            "writing-assistant",
            "diary-assistant",
            "diary-note",
            "note-to-blog",
            "biweekly-collector",
            "anki-card-generator",
        },
    },
    "creative-fun": {
        "category": "Creativity",
        "skills": {"zaregoto-miko"},
    },
}


class PluginRepositoryContractTest(unittest.TestCase):
    def test_marketplace_publishes_expected_plugins_in_order(self) -> None:
        marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))

        self.assertEqual(marketplace["name"], "niracler-skills")
        self.assertEqual(
            marketplace["interface"]["displayName"], "Niracler Skills"
        )
        self.assertEqual(
            [entry["name"] for entry in marketplace["plugins"]],
            list(EXPECTED_PLUGINS),
        )

        for entry in marketplace["plugins"]:
            plugin_name = entry["name"]
            self.assertEqual(
                entry["source"],
                {"source": "local", "path": f"./plugins/{plugin_name}"},
            )
            self.assertEqual(
                entry["policy"],
                {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            )
            self.assertEqual(
                entry["category"], EXPECTED_PLUGINS[plugin_name]["category"]
            )

    def test_plugins_publish_each_skill_exactly_once(self) -> None:
        published_skills: list[str] = []

        for plugin_name, expected in EXPECTED_PLUGINS.items():
            plugin_root = REPO_ROOT / "plugins" / plugin_name
            manifest = json.loads(
                (plugin_root / ".codex-plugin" / "plugin.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest["name"], plugin_name)
            self.assertEqual(manifest["version"], "0.1.0")
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["author"]["name"], "Niracler")
            self.assertEqual(
                manifest["interface"]["category"], expected["category"]
            )
            self.assertNotIn("apps", manifest)
            self.assertNotIn("mcpServers", manifest)
            self.assertNotIn("hooks", manifest)

            skill_names = {
                path.parent.name
                for path in (plugin_root / "skills").glob("*/SKILL.md")
            }
            self.assertEqual(skill_names, expected["skills"])
            published_skills.extend(skill_names)

        self.assertEqual(len(published_skills), 18)
        self.assertEqual(len(published_skills), len(set(published_skills)))

    def test_legacy_aggregate_layout_is_removed(self) -> None:
        self.assertFalse((REPO_ROOT / ".codex-plugin").exists())
        self.assertFalse((REPO_ROOT / "skills").exists())


if __name__ == "__main__":
    unittest.main()
