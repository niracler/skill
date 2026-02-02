#!/usr/bin/env bash
set -euo pipefail

# stats.sh - Collect git statistics from ~/code repos and output JSON
# Usage: stats.sh --since YYYY-MM-DD --until YYYY-MM-DD [--author <name|email>]

# --- Argument parsing ---

SINCE=""
UNTIL=""
AUTHOR=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --since) SINCE="$2"; shift 2 ;;
        --until) UNTIL="$2"; shift 2 ;;
        --author) AUTHOR="$2"; shift 2 ;;
        *) echo "Error: unknown argument: $1" >&2; exit 1 ;;
    esac
done

if [[ -z "$SINCE" || -z "$UNTIL" ]]; then
    echo "Usage: stats.sh --since YYYY-MM-DD --until YYYY-MM-DD [--author <name|email>]" >&2
    exit 1
fi

# Default author to git config user.name
if [[ -z "$AUTHOR" ]]; then
    AUTHOR=$(git config user.name 2>/dev/null || echo "")
fi

# --- Date handling ---
# git log --until is exclusive (before, not on), so add 1 day to include
# commits on the --until date itself.
next_day() {
    date -j -v+1d -f "%Y-%m-%d" "$1" "+%Y-%m-%d" 2>/dev/null || \
        date -d "$1 + 1 day" "+%Y-%m-%d" 2>/dev/null
}
# Append local timezone offset to bare dates so git interprets them correctly.
# Without this, git --since/--until with bare "YYYY-MM-DD" can misparse the timezone.
TZ_OFFSET=$(date '+%z')
TZ_OFFSET_ISO="${TZ_OFFSET:0:3}:${TZ_OFFSET:3:2}"

GIT_SINCE="${SINCE}T00:00:00${TZ_OFFSET_ISO}"
GIT_UNTIL="$(next_day "$UNTIL")T00:00:00${TZ_OFFSET_ISO}"

# --- Helpers ---

json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    printf '%s' "$s"
}

# --- Collect candidate directories ---

candidates=()
for dir in "$HOME"/code/*/; do
    [[ -d "$dir" ]] && candidates+=("$dir")
done
for dir in "$HOME"/code/*/repos/*/; do
    [[ -d "$dir" ]] && candidates+=("$dir")
done

# --- Scan repos and collect statistics ---

repos_scanned=0
repos_active=0
total_commits=0
total_insertions=0
total_deletions=0
first=true

echo "{"
printf '  "period": {"from": "%s", "to": "%s"},\n' "$SINCE" "$UNTIL"
echo '  "repos": ['

for dir in "${candidates[@]}"; do
    # Skip non-git directories
    [[ -d "${dir}.git" ]] || continue
    repos_scanned=$((repos_scanned + 1))

    # Build git log filter args
    log_args=(--since="$GIT_SINCE" --until="$GIT_UNTIL")
    [[ -n "$AUTHOR" ]] && log_args+=(--author="$AUTHOR")

    # Commit count
    commits=$(git -C "$dir" rev-list --count "${log_args[@]}" HEAD 2>/dev/null || echo "0")

    # Skip repos with zero commits (counted in repos_scanned but not in repos array)
    [[ "$commits" -eq 0 ]] && continue
    repos_active=$((repos_active + 1))

    # Author timestamps: newest first, oldest last
    timestamps=$(git -C "$dir" log "${log_args[@]}" --format="%aI" 2>/dev/null || echo "")
    first_commit=$(echo "$timestamps" | tail -1)
    last_commit=$(echo "$timestamps" | head -1)

    # Unique authors as JSON array
    authors_json="["
    afirst=true
    while IFS= read -r a; do
        [[ -z "$a" ]] && continue
        $afirst && afirst=false || authors_json+=","
        authors_json+="\"$(json_escape "$a")\""
    done < <(git -C "$dir" log "${log_args[@]}" --format="%an" 2>/dev/null | sort -u)
    authors_json+="]"

    # Numstat aggregation: insertions, deletions, unique files changed
    stats_line=$(
        git -C "$dir" log "${log_args[@]}" --numstat --format="" 2>/dev/null | \
        awk 'NF>=3 && $1!="-" {
            ins+=$1; del+=$2; files[$3]=1
        }
        END { fc=0; for(f in files) fc++; printf "%d %d %d", ins, del, fc }'
    ) || stats_line="0 0 0"
    read -r insertions deletions files_changed <<< "$stats_line"

    # Accumulate totals
    total_commits=$((total_commits + commits))
    total_insertions=$((total_insertions + insertions))
    total_deletions=$((total_deletions + deletions))

    # Output repo JSON entry
    path_clean="${dir%/}"
    name=$(basename "$dir")
    remote_url=$(git -C "$dir" config remote.origin.url 2>/dev/null || echo "")

    $first && first=false || printf ',\n'
    printf '    {"name":"%s","path":"%s","remote_url":"%s","commits":%d,"insertions":%d,"deletions":%d,"files_changed":%d,"authors":%s,"first_commit":"%s","last_commit":"%s"}' \
        "$(json_escape "$name")" \
        "$(json_escape "$path_clean")" \
        "$(json_escape "$remote_url")" \
        "$commits" \
        "$insertions" \
        "$deletions" \
        "$files_changed" \
        "$authors_json" \
        "$(json_escape "$first_commit")" \
        "$(json_escape "$last_commit")"
done

echo ""
echo "  ],"
printf '  "totals": {"repos_active": %d, "repos_scanned": %d, "commits": %d, "insertions": %d, "deletions": %d}\n' \
    "$repos_active" "$repos_scanned" "$total_commits" "$total_insertions" "$total_deletions"
echo "}"
