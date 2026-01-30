#!/bin/bash
# Validate all skills in the repository

echo "🔍 Validating skills..."
echo ""

found_skills=false
has_errors=false

for skill_dir in skills/*/SKILL.md; do
    if [ -f "$skill_dir" ]; then
        found_skills=true
        skill_name=$(dirname "$skill_dir")
        echo "Checking: $skill_name"

        if python3 scripts/quick_validate.py "$skill_name"; then
            echo "✅ $skill_name is valid"
        else
            echo "❌ $skill_name has errors"
            has_errors=true
        fi
        echo ""
    fi
done

if [ "$found_skills" = false ]; then
    echo "⚠️  No skills found"
    exit 1
fi

if [ "$has_errors" = true ]; then
    echo "❌ Some skills have validation errors"
    exit 1
else
    echo "✅ All skills are valid!"
    exit 0
fi
