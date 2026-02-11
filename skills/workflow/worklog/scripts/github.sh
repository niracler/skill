#!/usr/bin/env bash
set -euo pipefail

# github.sh - Collect GitHub PR and Issue activity, output JSON
# Usage: github.sh --since YYYY-MM-DD --until YYYY-MM-DD [--username <github-username>]

# --- Argument parsing ---

SINCE=""
UNTIL=""
USERNAME=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --since) SINCE="$2"; shift 2 ;;
        --until) UNTIL="$2"; shift 2 ;;
        --username) USERNAME="$2"; shift 2 ;;
        *) echo "Error: unknown argument: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$SINCE" || -z "$UNTIL" ]]; then
    echo "Usage: github.sh --since YYYY-MM-DD --until YYYY-MM-DD [--username <github-username>]" >&2
    exit 1
fi

# --- Check gh authentication ---
if ! gh auth status &>/dev/null; then
    echo "Error: gh CLI is not authenticated. Run 'gh auth login' first." >&2
    exit 1
fi

# --- Default username ---
if [[ -z "$USERNAME" ]]; then
    USERNAME=$(gh api user --jq '.login' 2>/dev/null) || {
        echo "Error: could not determine GitHub username. Pass --username or authenticate gh." >&2
        exit 1
    }
fi

# --- Temp directory for intermediate data ---
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

# --- Helpers ---

json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    printf '%s' "$s"
}

# --- Collect PRs ---
# Query scope (per spec D8):
#   1. PRs created in the period
#   2. PRs merged in the period (may have been created earlier)
#   3. Currently open PRs by the user
# Output as TSV via gh --jq, then deduplicate by repo+number with awk.

PR_FIELDS="repository,number,title,state,createdAt,closedAt"
# For merged PRs, closedAt = merge time. For open PRs, closedAt is a zero value — output "".
PR_JQ='.[] | [.repository.nameWithOwner, (.number | tostring), .title, (.state | ascii_downcase), .createdAt, (if (.state | ascii_downcase) == "merged" then .closedAt else "" end)] | @tsv'

{
    gh search prs --author="$USERNAME" --created="$SINCE..$UNTIL" \
        --json "$PR_FIELDS" --limit 100 --jq "$PR_JQ" 2>/dev/null || true
    gh search prs --author="$USERNAME" --merged-at="$SINCE..$UNTIL" \
        --json "$PR_FIELDS" --limit 100 --jq "$PR_JQ" 2>/dev/null || true
    gh search prs --author="$USERNAME" --state=open \
        --json "$PR_FIELDS" --limit 100 --jq "$PR_JQ" 2>/dev/null || true
} | awk -F'\t' 'NF>0 && !seen[$1 FS $2]++' > "$WORK_DIR/prs.tsv"

# --- Collect Issues ---
# Query: issues created in the period by the user.

ISSUE_FIELDS="repository,number,title,state,createdAt"
ISSUE_JQ='.[] | [.repository.nameWithOwner, (.number | tostring), .title, (.state | ascii_downcase), .createdAt] | @tsv'

gh search issues --author="$USERNAME" --created="$SINCE..$UNTIL" \
    --json "$ISSUE_FIELDS" --limit 100 --jq "$ISSUE_JQ" 2>/dev/null \
    > "$WORK_DIR/issues.tsv" || true

# --- Build JSON output ---

prs_merged=0
prs_open=0
issues_opened=0
issues_closed=0

echo "{"
printf '  "period": {"from": "%s", "to": "%s"},\n' "$SINCE" "$UNTIL"

# PRs array
echo '  "prs": ['
first=true
while IFS=$'\t' read -r repo number title state created_at merged_at; do
    [[ -z "$repo" ]] && continue
    $first && first=false || printf ',\n'
    printf '    {"repo":"%s","number":%s,"title":"%s","state":"%s","created_at":"%s","merged_at":"%s"}' \
        "$(json_escape "$repo")" "$number" "$(json_escape "$title")" "$state" "$created_at" "$merged_at"
    [[ "$state" == "merged" ]] && prs_merged=$((prs_merged + 1))
    [[ "$state" == "open" ]] && prs_open=$((prs_open + 1))
done < "$WORK_DIR/prs.tsv"
echo ""
echo "  ],"

# Issues array
echo '  "issues": ['
first=true
while IFS=$'\t' read -r repo number title state created_at; do
    [[ -z "$repo" ]] && continue
    $first && first=false || printf ',\n'
    printf '    {"repo":"%s","number":%s,"title":"%s","state":"%s","created_at":"%s"}' \
        "$(json_escape "$repo")" "$number" "$(json_escape "$title")" "$state" "$created_at"
    issues_opened=$((issues_opened + 1))
    [[ "$state" == "closed" ]] && issues_closed=$((issues_closed + 1))
done < "$WORK_DIR/issues.tsv"
echo ""
echo "  ],"

# Totals
printf '  "totals": {"prs_merged": %d, "prs_open": %d, "issues_opened": %d, "issues_closed": %d}\n' \
    "$prs_merged" "$prs_open" "$issues_opened" "$issues_closed"
echo "}"
