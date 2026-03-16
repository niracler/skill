#!/usr/bin/env python3
"""Workspace planning CLI — deterministic YAML operations for schedule management."""

import argparse
import json
import math
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


VALID_STATUSES = {"planned", "in_progress", "done", "deferred"}
TRANSITIONS = {
    "planned": {"in_progress", "deferred"},
    "in_progress": {"done"},
    "deferred": {"planned", "in_progress"},
    "done": set(),
}


def find_schedule(path: str | None) -> Path:
    """Find a schedule YAML file. If path is given, use it; otherwise scan."""
    if path:
        p = Path(path)
        if p.exists():
            return p
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    candidates = sorted(Path("planning/schedules").glob("*.yaml"))
    if not candidates:
        print("Error: no schedule YAML found in planning/schedules/", file=sys.stderr)
        sys.exit(1)
    if len(candidates) == 1:
        return candidates[0]

    print("Multiple schedules found:", file=sys.stderr)
    for i, c in enumerate(candidates):
        print(f"  {i + 1}. {c.name}", file=sys.stderr)
    print("Use --file to specify one.", file=sys.stderr)
    sys.exit(1)


def load_schedule(path: Path) -> dict:
    """Load and return the schedule YAML."""
    with open(path) as f:
        return yaml.safe_load(f)


def save_schedule(path: Path, data: dict) -> None:
    """Write schedule data back to YAML, preserving readability."""
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def find_module(data: dict, module_id: str) -> dict | None:
    """Find a module by id."""
    for m in data.get("modules", []):
        if m["id"] == module_id:
            return m
    return None


def current_week(data: dict) -> int:
    """Calculate current week number from timeline.start."""
    start = data["timeline"]["start"]
    if isinstance(start, str):
        start = datetime.strptime(start, "%Y-%m-%d").date()
    delta = (date.today() - start).days
    return max(1, math.ceil(delta / 7))


def cmd_review(args: argparse.Namespace) -> None:
    """Show overall schedule progress grouped by phase."""
    path = find_schedule(args.file)
    data = load_schedule(path)

    week = current_week(data)
    project = data.get("title", data.get("project", path.stem))

    result = {
        "project": project,
        "current_week": f"W{week}",
        "phases": [],
    }

    phases = {p["id"]: p for p in data.get("phases", [])}
    modules = data.get("modules", [])

    # Group modules by phase
    phase_modules: dict[str, list] = {}
    for m in modules:
        pid = m.get("phase", "unassigned")
        phase_modules.setdefault(pid, []).append(m)

    for pid, mods in phase_modules.items():
        phase_info = phases.get(pid, {"id": pid, "title": pid})
        done_count = sum(1 for m in mods if m["status"] == "done")
        total = len(mods)

        phase_result = {
            "id": pid,
            "title": phase_info.get("title", pid),
            "progress": f"{done_count}/{total}",
            "modules": [],
        }

        status_icon = {"done": "V", "in_progress": "*", "planned": "o", "deferred": "-"}
        for m in mods:
            icon = status_icon.get(m["status"], "?")
            type_info = m["type"]
            if m["type"] == "feature":
                type_info += f" {m.get('frames', '?')}f"
            phase_result["modules"].append({
                "icon": icon,
                "id": m["id"],
                "title": m["title"],
                "type": type_info,
                "status": m["status"],
            })

        result["phases"].append(phase_result)

    # Risks
    risks = []
    for m in modules:
        if m.get("design") in ("partial", "pending"):
            risks.append(f"Module '{m['id']}' has design status: {m['design']}")
    for milestone in data.get("milestones", []):
        ms_date = milestone["date"]
        if isinstance(ms_date, str):
            ms_date = datetime.strptime(ms_date, "%Y-%m-%d").date()
        days_left = (ms_date - date.today()).days
        if 0 < days_left <= 14:
            risks.append(f"Milestone '{milestone['id']}' in {days_left} days")

    result["risks"] = risks

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


def cmd_update(args: argparse.Namespace) -> None:
    """Update a module's status."""
    path = find_schedule(args.file)
    data = load_schedule(path)

    module = find_module(data, args.module_id)
    if not module:
        print(f"Error: module '{args.module_id}' not found", file=sys.stderr)
        sys.exit(1)

    current = module["status"]
    target = args.status

    if target not in VALID_STATUSES:
        print(f"Error: invalid status '{target}'. Valid: {VALID_STATUSES}", file=sys.stderr)
        sys.exit(1)

    if target not in TRANSITIONS[current]:
        allowed = TRANSITIONS[current] or {"(none — done is terminal)"}
        print(
            f"Error: cannot transition '{args.module_id}' from '{current}' to '{target}'. "
            f"Allowed: {allowed}",
            file=sys.stderr,
        )
        sys.exit(1)

    module["status"] = target
    save_schedule(path, data)

    result = {"module": args.module_id, "from": current, "to": target}
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


def cmd_link(args: argparse.Namespace) -> None:
    """Link an OpenSpec change to a module."""
    path = find_schedule(args.file)
    data = load_schedule(path)

    module = find_module(data, args.module_id)
    if not module:
        print(f"Error: module '{args.module_id}' not found", file=sys.stderr)
        sys.exit(1)

    change_name = args.change

    # Verify change exists
    change_dir = Path(f"openspec/changes/{change_name}")
    if not change_dir.exists():
        print(f"Error: openspec change '{change_name}' not found at {change_dir}", file=sys.stderr)
        sys.exit(1)

    changes = module.get("changes", [])
    if changes is None:
        changes = []
    if change_name in changes:
        print(f"Warning: '{change_name}' already linked to '{args.module_id}'", file=sys.stderr)
    else:
        changes.append(change_name)
        module["changes"] = changes

    # Auto-transition planned → in_progress
    auto_transitioned = False
    if module["status"] == "planned":
        module["status"] = "in_progress"
        auto_transitioned = True

    save_schedule(path, data)

    result = {
        "module": args.module_id,
        "change": change_name,
        "changes": changes,
        "auto_transitioned": auto_transitioned,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


def cmd_week(args: argparse.Namespace) -> None:
    """Show modules relevant to a specific week."""
    path = find_schedule(args.file)
    data = load_schedule(path)

    target_week = args.week

    backend_modules = []
    frontend_modules = []

    for m in data.get("modules", []):
        weeks = m.get("weeks", [])
        ready_week = m.get("backend", {}).get("ready_week") if isinstance(m.get("backend"), dict) else None
        mock_from = m.get("frontend", {}).get("mock_from") if isinstance(m.get("frontend"), dict) else None

        relevant = target_week in weeks or ready_week == target_week or mock_from == target_week

        if relevant:
            if m["type"] == "infrastructure" or ready_week == target_week:
                backend_modules.append(m)
            if m["type"] == "feature" and (mock_from == target_week or target_week in weeks):
                frontend_modules.append(m)

    result = {
        "week": target_week,
        "backend": [{"id": m["id"], "title": m["title"], "status": m["status"]} for m in backend_modules],
        "frontend": [{"id": m["id"], "title": m["title"], "status": m["status"]} for m in frontend_modules],
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Workspace planning CLI")
    parser.add_argument("--file", "-f", help="Path to schedule YAML file")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("review", help="Show schedule progress")

    p_update = sub.add_parser("update", help="Update module status")
    p_update.add_argument("module_id", help="Module ID")
    p_update.add_argument("--status", "-s", required=True, help="Target status")

    p_link = sub.add_parser("link", help="Link OpenSpec change to module")
    p_link.add_argument("module_id", help="Module ID")
    p_link.add_argument("--change", "-c", required=True, help="OpenSpec change name")

    p_week = sub.add_parser("week", help="Show modules for a specific week")
    p_week.add_argument("week", help="Week identifier (e.g. W3)")

    args = parser.parse_args()

    commands = {
        "review": cmd_review,
        "update": cmd_update,
        "link": cmd_link,
        "week": cmd_week,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
