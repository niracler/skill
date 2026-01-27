#!/bin/bash
# Check Calendar and Reminders permissions for osascript

echo "=== Schedule Manager Permission Check ==="
echo ""

# Check Calendar permission
echo "Checking Calendar access..."
calendar_result=$(osascript -e 'tell application "Calendar" to get name of first calendar' 2>&1)
if [[ "$calendar_result" == *"error"* ]] || [[ "$calendar_result" == *"not allowed"* ]]; then
    echo "❌ Calendar: Permission denied"
    echo "   Fix: System Settings → Privacy & Security → Calendar → Enable Terminal/Claude"
else
    echo "✅ Calendar: OK ($calendar_result)"
fi

echo ""

# Check Reminders permission
echo "Checking Reminders access..."
reminders_result=$(osascript -e 'tell application "Reminders" to get name of first list' 2>&1)
if [[ "$reminders_result" == *"error"* ]] || [[ "$reminders_result" == *"not allowed"* ]]; then
    echo "❌ Reminders: Permission denied"
    echo "   Fix: System Settings → Privacy & Security → Reminders → Enable Terminal/Claude"
else
    echo "✅ Reminders: OK ($reminders_result)"
fi

echo ""
echo "=== Check Complete ==="
