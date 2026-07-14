import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

EXPECTED_PLUGINS = {
    "developer-workflows": {
        "category": "Developer Tools",
        "skills": {
            "markdown-lint",
            "skill-reviewer",
        },
    },
    "personal-knowledge": {
        "category": "Knowledge & Files",
        "skills": {
            "anki-card-generator",
        },
    },
    "creative-fun": {
        "category": "Creativity",
        "skills": {"zaregoto-miko"},
    },
    "personal": {
        "category": "Productivity",
        "skills": {
            "writing-assistant",
            "note-to-blog",
            "biweekly-collector",
            "weekly-report",
        },
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

        expected_skill_count = sum(
            len(plugin["skills"]) for plugin in EXPECTED_PLUGINS.values()
        )
        self.assertEqual(len(published_skills), expected_skill_count)
        self.assertEqual(len(published_skills), len(set(published_skills)))

    def test_legacy_aggregate_layout_is_removed(self) -> None:
        self.assertFalse((REPO_ROOT / ".codex-plugin").exists())
        self.assertFalse((REPO_ROOT / "skills").exists())

    def test_personal_skills_use_chinese_instructions(self) -> None:
        skills_root = REPO_ROOT / "plugins" / "personal" / "skills"

        for skill_name in EXPECTED_PLUGINS["personal"]["skills"]:
            content = (skills_root / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            frontmatter = content.split("---", 2)[1]
            self.assertRegex(frontmatter, r"description:[\s\S]*[\u4e00-\u9fff]")

            in_fence = False
            headings: list[str] = []
            for line in content.splitlines():
                if line.startswith("```"):
                    in_fence = not in_fence
                elif not in_fence and line.startswith("#"):
                    headings.append(line)

            self.assertTrue(headings, f"{skill_name} must contain headings")
            for heading in headings:
                self.assertRegex(
                    heading,
                    r"[\u4e00-\u9fff]",
                    f"{skill_name} heading must use Chinese: {heading}",
                )


if __name__ == "__main__":
    unittest.main()
