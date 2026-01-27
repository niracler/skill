#!/bin/bash
# Check dependencies for schedule-manager skill

echo "=== Schedule Manager Dependency Check ==="
echo ""

# Check osascript (always available on macOS)
echo "Checking osascript..."
if command -v osascript &> /dev/null; then
    echo "✅ osascript: OK (built-in)"
else
    echo "❌ osascript: Not found (this should not happen on macOS)"
fi

echo ""

# Check icalBuddy (optional but recommended)
echo "Checking icalBuddy..."
if command -v icalBuddy &> /dev/null; then
    version=$(icalBuddy --version 2>&1 | head -1)
    echo "✅ icalBuddy: OK ($version)"
else
    echo "⚠️  icalBuddy: Not installed (optional but recommended)"
    echo "   Install: brew install ical-buddy"
    echo "   Benefits: Better recurring event support"
fi

echo ""

# Check Homebrew (needed for icalBuddy installation)
echo "Checking Homebrew..."
if command -v brew &> /dev/null; then
    echo "✅ Homebrew: OK"
else
    echo "ℹ️  Homebrew: Not installed"
    echo "   Install: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

echo ""
echo "=== Check Complete ==="
