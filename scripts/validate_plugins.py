#!/usr/bin/env python3
"""Validate this repository's Codex marketplace and bundled plugins."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SKILL_NAME_RE = re.compile(r"^name:\s*([^\s]+)\s*$", re.MULTILINE)
INSTALL_POLICIES = {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}
AUTH_POLICIES = {"ON_INSTALL", "ON_USE"}


def load_json_object(
    path: Path, label: str, errors: list[str]
) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label} must contain valid JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label} must contain a JSON object")
        return None
    return payload


def validate_repository(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    plugins_root = repo_root / "plugins"
    errors: list[str] = []
    marketplace = load_json_object(
        repo_root / ".agents" / "plugins" / "marketplace.json",
        "marketplace.json",
        errors,
    )
    if marketplace is None:
        return errors

    marketplace_name = marketplace.get("name")
    if not isinstance(marketplace_name, str) or not marketplace_name.strip():
        errors.append("marketplace.json field `name` must be a non-empty string")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        errors.append("marketplace.json field `plugins` must be an array")
        return errors

    seen_plugins: set[str] = set()
    seen_skills: set[str] = set()
    published_dirs: set[str] = set()
    for index, raw_entry in enumerate(entries):
        label = f"marketplace.json plugins[{index}]"
        if not isinstance(raw_entry, dict):
            errors.append(f"{label} must be an object")
            continue

        name = raw_entry.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{label}.name must be a non-empty string")
            continue
        if name in seen_plugins:
            errors.append(f"duplicate plugin name `{name}` in marketplace.json")
        seen_plugins.add(name)

        source = raw_entry.get("source")
        if not isinstance(source, dict) or source.get("source") != "local":
            errors.append(f"{label}.source must describe a local plugin")
            continue
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path.startswith("./plugins/"):
            errors.append(f"{label}.source.path must stay under `./plugins/`")
            continue

        plugin_root = (repo_root / source_path[2:]).resolve()
        try:
            plugin_root.relative_to(plugins_root.resolve())
        except ValueError:
            errors.append(f"{label}.source.path must stay under `./plugins/`")
            continue

        published_dirs.add(plugin_root.name)
        if plugin_root.name != name:
            errors.append(
                f"{label}.name `{name}` must match plugin directory `{plugin_root.name}`"
            )

        validate_policy(raw_entry, label, errors)
        skill_names = validate_plugin(plugin_root, name, errors)
        for skill_name in skill_names:
            if skill_name in seen_skills:
                errors.append(f"duplicate skill name `{skill_name}` across plugins")
            seen_skills.add(skill_name)

    if plugins_root.is_dir():
        actual_dirs = {
            path.name
            for path in plugins_root.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        }
        for unpublished in sorted(actual_dirs - published_dirs):
            errors.append(
                f"plugin directory `{unpublished}` is not listed in marketplace.json"
            )

    return errors


def validate_policy(entry: dict[str, Any], label: str, errors: list[str]) -> None:
    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"{label}.policy must be an object")
        return
    if policy.get("installation") not in INSTALL_POLICIES:
        errors.append(f"{label}.policy.installation is invalid")
    if policy.get("authentication") not in AUTH_POLICIES:
        errors.append(f"{label}.policy.authentication is invalid")
    category = entry.get("category")
    if not isinstance(category, str) or not category.strip():
        errors.append(f"{label}.category must be a non-empty string")


def validate_plugin(
    plugin_root: Path, expected_name: str, errors: list[str]
) -> set[str]:
    if not plugin_root.is_dir():
        errors.append(f"plugin directory is missing: {plugin_root}")
        return set()

    manifest = load_json_object(
        plugin_root / ".codex-plugin" / "plugin.json",
        f"plugin `{expected_name}` manifest",
        errors,
    )
    if manifest is None:
        return set()

    manifest_name = manifest.get("name")
    if manifest_name != plugin_root.name:
        errors.append(
            f"plugin manifest name `{manifest_name}` must match plugin directory "
            f"`{plugin_root.name}`"
        )
    if manifest_name != expected_name:
        errors.append(
            f"plugin manifest name `{manifest_name}` must match marketplace name "
            f"`{expected_name}`"
        )

    version = manifest.get("version")
    if not isinstance(version, str) or SEMVER_RE.fullmatch(version) is None:
        errors.append(f"plugin `{expected_name}` version must use strict SemVer")
    if manifest.get("skills") != "./skills/":
        errors.append(f"plugin `{expected_name}` field `skills` must be `./skills/`")

    skills_root = plugin_root / "skills"
    skill_names = validate_skills(skills_root, expected_name, errors)

    for field in ("apps", "mcpServers"):
        reference = manifest.get(field)
        if isinstance(reference, str):
            validate_reference(plugin_root, reference, f"plugin.{field}", errors)

    interface = manifest.get("interface")
    if isinstance(interface, dict):
        for field in ("composerIcon", "logo", "logoDark"):
            reference = interface.get(field)
            if isinstance(reference, str):
                validate_reference(
                    plugin_root, reference, f"interface.{field}", errors
                )
        screenshots = interface.get("screenshots", [])
        if isinstance(screenshots, list):
            for index, reference in enumerate(screenshots):
                if isinstance(reference, str):
                    validate_reference(
                        plugin_root,
                        reference,
                        f"interface.screenshots[{index}]",
                        errors,
                    )

    return skill_names


def validate_skills(
    skills_root: Path, plugin_name: str, errors: list[str]
) -> set[str]:
    if not skills_root.is_dir():
        errors.append(f"plugin `{plugin_name}` is missing its `skills/` directory")
        return set()

    skill_dirs = [path for path in skills_root.iterdir() if path.is_dir()]
    if not skill_dirs:
        errors.append(f"plugin `{plugin_name}` has no bundled skills")
        return set()

    skill_names: set[str] = set()
    for skill_root in sorted(skill_dirs):
        skill_md = skill_root / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"skill `{skill_root.name}` is missing SKILL.md")
            continue
        match = SKILL_NAME_RE.search(skill_md.read_text(encoding="utf-8"))
        if match is None:
            errors.append(f"skill `{skill_root.name}` is missing frontmatter name")
            continue
        declared_name = match.group(1)
        if declared_name != skill_root.name:
            errors.append(
                f"skill name `{declared_name}` must match directory `{skill_root.name}`"
            )
        skill_names.add(declared_name)
    return skill_names


def validate_reference(
    plugin_root: Path, raw_path: str, field: str, errors: list[str]
) -> None:
    if not raw_path.startswith("./"):
        errors.append(f"{field} must use a `./`-prefixed relative path")
        return
    target = (plugin_root / raw_path[2:]).resolve()
    try:
        target.relative_to(plugin_root.resolve())
    except ValueError:
        errors.append(f"{field} must stay inside the plugin directory")
        return
    if not target.is_file():
        errors.append(f"{field} references a missing file: {raw_path}")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    errors = validate_repository(repo_root)
    if errors:
        print("Plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Plugin validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
