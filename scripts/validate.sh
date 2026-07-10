#!/usr/bin/env bash
# Validate bundled skills, Codex plugins, and repository contracts.

set -uo pipefail

echo "🔍 Validating skills..."
echo ""

found_skills=false
has_errors=false

shopt -s nullglob
skill_manifests=(plugins/*/skills/*/SKILL.md)

for skill_manifest in "${skill_manifests[@]}"; do
    if [ -f "$skill_manifest" ]; then
        found_skills=true
        skill_dir=$(dirname "$skill_manifest")
        echo "Checking: $skill_dir"

        if python3 scripts/quick_validate.py "$skill_dir"; then
            echo "✅ $skill_dir is valid"
        else
            echo "❌ $skill_dir has errors"
            has_errors=true
        fi
        echo ""
    fi
done

if [ "$found_skills" = false ]; then
    echo "⚠️  No skills found"
    exit 1
fi

echo "🔍 Validating Codex plugin contracts..."
if ! python3 scripts/validate_plugins.py; then
    has_errors=true
fi

echo ""
echo "🔍 Running repository contract tests..."
if ! python3 -m unittest discover -s tests -v; then
    has_errors=true
fi

if [ "$has_errors" = true ]; then
    echo "❌ Repository validation failed"
    exit 1
else
    echo "✅ Repository validation passed"
    exit 0
fi
