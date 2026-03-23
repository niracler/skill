---
name: biweekly-collector
description: >-
  Use this skill to collect and organize materials for writing a personal biweekly
  diary (双周记/周记). Invoke immediately when the user wants to: gather diary materials
  from the past 2-4 weeks, prepare content for their 周记, review what happened recently
  for journaling, or compile life events + media consumption + articles into a structured
  draft. Trigger phrases: 收集双周记素材, 准备周记, 周记素材, 双周记, biweekly materials,
  gather journal materials, 最近发生了什么, 整理素材写周记. This skill collects raw materials
  from multiple sources (daily notes, Pinboard, Douban, Telegram, Calendar, Reminders,
  Photos, RSS digests, plrom diff) and organizes them into the 周记 template structure —
  it does NOT write the final diary for you. Distinct from diary-assistant (daily journaling),
  weekly-report (work report for boss), and diary-note (quick append).
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["curl","osascript","reminders-cli","git"],"env":["PINBOARD_AUTH_TOKEN"]}}}
---

# Biweekly Collector

收集双周记写作素材。从日记、书签、豆瓣、Telegram、日历、提醒事项、照片、RSS 精选、plrom 变更等
多个来源抓取过去 2-4 周的素材，整理成周记模板结构，供用户手写周记时参考。

**这个 skill 不代写周记** — 周记的灵魂在于你自己的文字和反思。它只负责把散落各处的碎片聚合起来，
让你写的时候不遗漏重要的事。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| macOS | system | Yes | This skill requires macOS |
| reminders-cli | cli | Yes | `brew install keith/formulae/reminders-cli` |
| curl | cli | Yes | Built-in on macOS |
| git | cli | Yes | Built-in or `brew install git` |
| `PINBOARD_AUTH_TOKEN` | env var | Yes | See pinboard-manager skill for setup |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing
> tool, skip that data source and continue with what's available.

## Key Paths

| Path | Purpose |
|------|---------|
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/Archives/日记(Daily)/` | Daily diary entries |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/Areas/生活(Life)/周记(Weekly)/` | Output location for 周记 |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/templates/monthly.md` | 周记 template |
| `~/code/ai-dev/repos/rss-agent/output/daily/` | AI-curated RSS daily digests |
| `~/code/nini-dev/repos/plrom/README.md` | plrom source file (人 X 社区 X 物), has its own git repo |

## Workflow Overview

```text
┌──────────────────────────────────────────────────────────────┐
│           biweekly-collector 完整流程（~15-20min）              │
└──────────────────────────────────────────────────────────────┘

  ┌──────────────────┐
  │ 用户触发素材收集   │
  └──────┬───────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 1. 确认时间范围 + 创建文件  (~2min) │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────────┐
  │ 2. 并行数据收集（subagent）      (~5-8min)   │
  │    ┌─ 日记条目提取                           │
  │    ├─ Pinboard 书签                          │
  │    ├─ 豆瓣动态 (RSS)                         │
  │    ├─ Telegram 频道 (RSS)                    │
  │    ├─ Apple Calendar 事件                    │
  │    ├─ Apple Reminders 完成项                 │
  │    ├─ RSS 精选摘要                           │
  │    └─ plrom git diff                         │
  └──────┬──────────────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 3. 整理素材到模板结构      (~3min)  │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 4. 展示 + 用户确认写入     (~3min)  │
  └──────┬─────────────────────────────┘
         │
         ▼
      ┌──────┐
      │ 完成  │
      └──────┘
```

## Step 1: Confirm Period and Create File

### Determine Time Range

The biweekly diary covers a flexible period (2-4 weeks). Ask the user:

```text
Claude: 「这次周记要覆盖什么时间段？」
        建议：3/10 - 3/23（两周）
        或者你可以指定其他范围（最短两周，最长一个月）
```

Suggest a default based on the last 周记's date. Scan `Areas/生活(Life)/周记(Weekly)/` for the
most recent entry to calculate the gap.

### Determine Title

The 周记 naming convention is `YYYYMM-N-title.md`:
- `YYYYMM`: year-month of the period's end date
- `N`: the nth entry of that month (1, 2, 3...)
- `title`: a short descriptive title chosen by the user

Ask the user for a title, or offer to decide later after seeing the materials.

### Create Skeleton File

Create the file in the 周记 directory using the template from `templates/monthly.md`:

```markdown
---
aliases:
tags:
  - 周记
date: {start_date}
modified: {today}
---

> {用户稍后填写的开场白}

## 关于现实生活的记录

> [!info]
> 我所有的周记或许并没有谎言，起码没有主动撒谎的部分。但其中的内容可能都具有某种倾向性，例如隐藏了某些未言明的黑暗成分，或者说是选择性的表达。

<!-- 以下是收集到的素材，请根据这些素材手写正文 -->

### 素材：生活事件与日记摘要

{collected_diary_materials}

### 素材：日历事件

{collected_calendar_events}

### 素材：完成的提醒事项

{collected_reminders}

### 素材：plrom 变更

{collected_plrom_diff}

## 👀 还看了什么

### 📚 🎬 📺 作品

| 作品 & 产品名 | 媒介 | 进度 | 打分 | 吐槽 |
| -------- | --- | --- | --- | --- |
{collected_douban_entries}

### 🌐 文章

{collected_articles}

### 素材：RSS 精选回顾

{collected_rss_digests}

### 素材：Telegram 频道分享

{collected_telegram_posts}

## 后记

<!-- 这里是你的个人反思空间 -->
```

## Step 2: Parallel Data Collection

Launch subagents for each data source concurrently. Each source is independent — if one fails,
skip it and continue.

### 2a. Daily Diary Entries

Read each daily note within the date range from `Archives/日记(Daily)/`.

Extract content from three sections:
- `## 1 title Journal` → personal events, reflections, photos
- `## 2 Work Log` → skim for personal-interest items (skip formal 周报 content)
- `## 3 Today I Learn` → TIL entries, media impressions

**Output format:**
```markdown
#### 3/10 (周一)
- 在图书馆看了《断舍离》
- 跟朋友 L 约了羽毛球

#### 3/11 (周二)
- Home Assistant Dashboard 大整理
- 看完了《迷宫饭》第二季
```

Preserve the user's original voice — summarize but don't rewrite. Include photo references
(`![[filename]]` or `![](url)`) as-is.

### 2b. Pinboard Bookmarks

Fetch bookmarks from the date range:

```bash
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json&fromdt={start_date}T00:00:00Z&todt={end_date}T23:59:59Z"
```

Format each bookmark as:
```markdown
- [Title](url) - {description if any} `{tags}`
```

Group by week or by tag category if there are many.

### 2c. Douban Activity (RSS)

Fetch the user's Douban interest feed. Try direct feed first, fall back to RSSHub:

```bash
# Try direct feed first
curl -s "https://www.douban.com/feed/people/niracler/interests"
# If empty or blocked, use RSSHub
curl -s "https://rsshub.app/douban/people/niracler/interests"
```

Parse the RSS/Atom entries. Extract:
- Title (作品名)
- Category/type (书/电影/音乐/游戏)
- Rating (if marked)
- Short comment (if any)
- Date

Format into the 作品 table rows:
```markdown
| 《作品名》 | 电影 | 100% | 8 | 用户的短评 |
```

If the Douban feed is unavailable or empty, note this and the user can fill manually.

### 2d. Telegram Channel (RSS)

Fetch the user's Telegram channel RSS:

```bash
curl -s "https://tg.niracler.com/rss.xml"
```

The feed is standard RSS 2.0 with `<content:encoded>` HTML bodies. Important parsing notes:

- **Title may be absent** — fall back to extracting first line of `<content:encoded>` text
- **Hashtags are inline** in HTML as `<a href="/search/...">` links (e.g., `#pinboard`, `#bilibili`,
  `#梦`, `#暴论`, `#网易云音乐`). Extract via regex for categorization.
- **pubDate** is in GMT (RFC 2822). **Strictly filter by date range** — only include items
  whose pubDate falls within the confirmed start/end dates. This is critical when the user
  specifies a historical range (e.g., 3/1-3/15) because the RSS feed contains recent posts
  that may be outside the range. Parse the date and compare before including.
- **Content types** vary: bookmarked articles, video shares, personal thoughts, dream journal,
  music shares, ACG content, tech observations, life updates

Use a script to filter strictly:
```bash
# Fetch and filter Telegram RSS by date range
curl -s "https://tg.niracler.com/rss.xml" | python3 -c "
import sys, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

start = datetime({start_year}, {start_month}, {start_day}, tzinfo=timezone.utc)
end = datetime({end_year}, {end_month}, {end_day}, 23, 59, 59, tzinfo=timezone.utc)

tree = ET.parse(sys.stdin)
for item in tree.findall('.//item'):
    pub = item.find('pubDate')
    if pub is not None:
        dt = parsedate_to_datetime(pub.text)
        if start <= dt <= end:
            title = item.find('title')
            link = item.find('link')
            print(f'{dt.strftime(\"%m/%d\")} | {title.text if title is not None and title.text else \"(untitled)\"} | {link.text}')
"
```

Group by hashtag category when possible:
```markdown
#### 文章分享 (#pinboard)
- [Article title](url) - user's comment

#### 随想 (#暴论)
- 3/15: "some thought..."

#### 其他
- 3/12: 新电脑到了
```

### 2e. Apple Calendar Events

Query Calendar events within the date range:

```applescript
osascript -e '
tell application "Calendar"
    set startDate to current date
    set time of startDate to 0
    -- calculate actual start/end dates
    set endDate to startDate
    set eventList to ""
    repeat with cal in calendars
        set calEvents to (every event of cal whose start date >= startDate and start date <= endDate)
        repeat with ev in calEvents
            set eventList to eventList & (start date of ev) & " | " & (summary of ev) & linefeed
        end repeat
    end repeat
    return eventList
end tell'
```

Calculate the actual date offsets from the confirmed period. Include personal calendar events
(meetups, appointments, trips) but skip recurring work meetings.

### 2f. Apple Reminders (Completed)

Query completed reminders within the date range:

```bash
reminders show-all --completed
```

Filter by date range. Completed personal tasks show what the user actually accomplished
beyond work — exercise goals, reading targets, errands.

### 2g. RSS Daily Digests

Read the AI-curated daily digest files from `~/code/ai-dev/repos/rss-agent/output/daily/`.

For each day in the range, read `YYYY-MM-DD.md` if it exists. Each daily digest contains:
- AI-scored articles (0-100) with Chinese summaries
- Two sections: "核心推荐" (4 core focus) and "开拓视野" (3 exploration)
- Each article has: title, source, score, reasoning, category, personal relevance

Extract the highest-scored articles (score >= 70) as "this period's reading highlights".
Deduplicate against Pinboard bookmarks (same URL = already captured via Pinboard).
Also deduplicate against Telegram channel shares (same URL).

### 2h. plrom Git Diff

The plrom repo (`~/code/nini-dev/repos/plrom/`) is a standalone git repo that tracks
"人 X 社区 X 物" — the user's curated list of people, communities, and things they follow.
It auto-syncs to the blog via GitHub Actions.

Check what changed during the period:

```bash
cd ~/code/nini-dev/repos/plrom
git log --since="{start_date}" --until="{end_date}" --oneline
# If there are commits, get the diff
FIRST_COMMIT=$(git log --since="{start_date}" --format="%H" --reverse | head -1)
if [ -n "$FIRST_COMMIT" ]; then
  git diff "$FIRST_COMMIT"^..HEAD -- README.md
fi
```

If there are changes, summarize what was added/removed:
- New people followed (技术博主, 漫画家, UP 主, etc.)
- New communities joined
- New tools/products/games discovered
- Items removed or moved to 弃坑列表

The plrom page has sections: 人 (技术博主/作家/漫画家/导演/UP主/TG芳邻/播客/歌手/淘宝店主),
组织或社区, 物 (软件/硬件/游戏). This captures the user's evolving interests and discoveries.

## Step 3: Organize into Template

After all data is collected, organize the materials into the skeleton file created in Step 1.

### Organization Rules

1. **生活事件** — merge diary entries + calendar events + completed reminders into a
   chronological narrative scaffold. Group related events (e.g., consecutive days of a trip).

2. **作品 table** — merge Douban entries with any media mentioned in diary TIL sections.
   Deduplicate by title. Keep the user's original comments when available.

3. **文章 section** — merge Pinboard bookmarks + RSS digest highlights + Telegram shares.
   Deduplicate by URL. Prefer Pinboard entries (they have the user's own description).
   Format like historical 周记 entries:
   ```markdown
   - [Title](url) - one-line comment from user or AI summary
   ```

4. **plrom diff** — present as a "discoveries" subsection showing what's new.

5. **Photos** — collect all `![[image]]` and `![](url)` references from diary entries.
   List them in context so the user can select which to include.

### What NOT to Do

- Do NOT write the actual 周记 prose — only organize raw materials
- Do NOT filter out events you think are unimportant — the user decides what matters
- Do NOT merge events that happened on different days without noting both dates
- Do NOT include formal work 周报 content (that's the weekly-report skill's domain)

## Step 4: Present and Confirm

Show the user a summary of what was collected:

```text
素材收集完成！以下是各来源的数量统计：

📔 日记条目: 12 天有内容
📌 Pinboard 书签: 8 条
🎬 豆瓣动态: 3 部作品
📱 Telegram 分享: 15 条
📅 日历事件: 6 个
✅ 完成的提醒: 9 项
📰 RSS 精选: 22 篇（去重后 17 篇）
🔄 plrom 变更: +3 新增, -1 移除

已写入文件：Areas/生活(Life)/周记(Weekly)/202603-2-title.md
你可以在 Obsidian 中打开这个文件，在素材基础上写你的周记。
```

Ask if the user wants to:
- Adjust the time range and re-collect
- Remove certain sections
- Add any manual notes they remembered

Write the final organized materials to the file.

## Data Source Degradation

| Source unavailable | Behavior |
|---|---|
| Daily notes missing for some days | Use available days, note gaps |
| Pinboard token not set | Skip, note "Pinboard 数据未获取" |
| Douban feed empty or blocked | Try RSSHub fallback: `https://rsshub.app/douban/people/niracler/interests`; if still empty, leave table for manual fill |
| Telegram RSS unreachable | Skip, note it |
| Calendar access denied | Skip, suggest `! tccutil reset Calendar` |
| rss-agent output missing | Skip, note "RSS 精选未找到" |
| plrom repo not found | Skip plrom diff |

## Common Issues

| Issue | Fix |
|-------|-----|
| Douban RSS returns empty | Douban may block direct RSS; try via RSSHub: `https://rsshub.app/douban/people/niracler/interests` |
| Calendar date math wrong | Use `current date` with day offsets in AppleScript, not string dates |
| Too many Pinboard results | Add tag filter or increase `fromdt` precision |
| plrom has no commits in range | Normal — plrom updates are infrequent |
| Telegram RSS has no date filter | Fetch all entries, filter by pubDate in the date range |
| File already exists | Ask user: overwrite / append / use different name |
