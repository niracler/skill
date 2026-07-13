---
name: biweekly-collector
description: >-
  用于收集和整理个人双周记或周记的素材。用户提出「收集双周记素材」「准备周记」
  「周记素材」「双周记」「最近发生了什么」「整理素材写周记」、"biweekly materials"
  或 "gather journal materials" 时立即使用。从日记、Pinboard、豆瓣、Telegram、
  Calendar、Reminders、照片、RSS 摘要和 plrom diff 中收集最近 2～4 周的原始材料，
  并按周记模板整理，但不代写最终正文。每日写作使用 diary-assistant，工作周报使用
  weekly-report，快速追记使用 diary-note。
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["curl","reminders-cli","git","icalBuddy"],"env":["PINBOARD_AUTH_TOKEN"]}}}
---

# 双周记素材收集器

收集双周记写作素材。从日记、书签、豆瓣、Telegram、日历、提醒事项、照片、RSS 精选、plrom 变更等
多个来源抓取过去 2-4 周的素材，整理成周记模板结构，供用户手写周记时参考。

**这个 skill 不代写周记。** 周记的核心是作者自己的文字和反思。这里只聚合散落素材，
减少写作时的遗漏。

## 前置条件

| 工具 | 类型 | 必需 | 安装方式 |
|------|------|----------|---------|
| macOS | 系统 | 是 | 此 skill 仅支持 macOS |
| reminders-cli | CLI | 是 | `brew install keith/formulae/reminders-cli` |
| icalBuddy | CLI | 是 | `brew install ical-buddy` |
| curl | CLI | 是 | macOS 内置 |
| Git | CLI | 是 | 系统内置或运行 `brew install git` |
| `PINBOARD_AUTH_TOKEN` | 环境变量 | 是 | 配置方式见 pinboard-manager skill |

> 加载 skill 时不要主动检查这些工具。命令因缺少工具而失败时，跳过对应数据源，
> 使用其余可用数据继续。

## 关键路径

| 路径 | 用途 |
|------|---------|
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/Archives/日记(Daily)/` | 每日日记 |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/Areas/生活(Life)/周记(Weekly)/` | 旧版周记输出目录 |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/Areas/生活(Life)/月记(Monthly)/` | 当前月记输出目录 |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/templates/monthly.md` | 周记模板 |
| `~/code/ai-dev/repos/rss-agent/output/daily/` | AI 筛选的 RSS 每日摘要 |
| `~/code/nini-dev/repos/plrom/README.md` | plrom「人 × 社区 × 物」源文件，使用独立 Git 仓库 |

## 工作流概览

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

## 步骤 1：确认周期并创建文件

### 确定时间范围

双周记允许覆盖 2～4 周。询问用户：

```text
Claude: 「这次周记要覆盖什么时间段？」
        建议：3/10 - 3/23（两周）
        或者你可以指定其他范围（最短两周，最长一个月）
```

根据上一篇记录的日期建议默认范围。扫描 `Areas/生活(Life)/周记(Weekly)/` 和
`Areas/生活(Life)/月记(Monthly)/`，以最近一篇记录计算间隔。

### 确定标题

周记文件名采用 `YYYYMM-N-title.md`：

- `YYYYMM`：周期结束日期所在的年月。
- `N`：当月第几篇记录，从 1 开始。
- `title`：用户选择的简短描述性标题。

询问标题，也可以在看完素材后再决定。

### 创建骨架文件

使用 `templates/monthly.md` 创建文件。输出目录可以是 `周记(Weekly)/` 或
`月记(Monthly)/`；询问用户，或直接采用用户指定的路径：

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

### 素材：当前提醒事项（个人相关）

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

## 步骤 2：并行收集数据

为每个数据源并行启动 subagent。各数据源相互独立；某个来源失败时跳过并继续。

### 2a：每日日记

读取 `Archives/日记(Daily)/` 中日期范围内的每篇日记。

从三个章节提取内容：

- `## 1 title Journal`：个人事件、反思和照片。
- `## 2 Work Log`：浏览与个人兴趣相关的内容，跳过正式周报。
- `## 3 Today I Learn`：TIL 和作品感想。

**输出格式：**

```markdown
#### 3/10 (周一)
- 在图书馆看了《断舍离》
- 跟朋友 L 约了羽毛球

#### 3/11 (周二)
- Home Assistant Dashboard 大整理
- 看完了《迷宫饭》第二季
```

保留用户原有语气，只整理摘要，不改写。照片引用 `![[filename]]` 或 `![](url)` 原样保留。

### 2b：Pinboard 书签

获取日期范围内的书签：

```bash
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json&fromdt={start_date}T00:00:00Z&todt={end_date}T23:59:59Z"
```

每条书签采用以下格式：

```markdown
- [Title](url) - {description if any} `{tags}`
```

数量较多时按周或标签分类。

### 2c：豆瓣动态（RSS）

获取用户的豆瓣兴趣动态。先访问直接订阅源，失败后使用 RSSHub：

```bash
# Try direct feed first
curl -s "https://www.douban.com/feed/people/niracler/interests"
# If empty or blocked, use RSSHub
curl -s "https://rsshub.app/douban/people/niracler/interests"
```

解析 RSS 或 Atom 条目，提取：

- 标题（作品名）
- 类型（书、电影、音乐或游戏）
- 评分（存在时）
- 短评（存在时）
- 日期

整理为作品表格行：

```markdown
| 《作品名》 | 电影 | 100% | 8 | 用户的短评 |
```

豆瓣订阅源不可用或为空时，标记该情况，由用户手动补充。

### 2d：Telegram 频道（RSS）

获取用户的 Telegram 频道 RSS：

```bash
curl -s "https://tg.niracler.com/rss.xml"
```

订阅源使用标准 RSS 2.0，正文是 `<content:encoded>` HTML。解析时注意：

- **标题可能缺失**：改用 `<content:encoded>` 文本的第一行。
- **Hashtag 位于 HTML 内部**：表现为 `<a href="/search/...">` 链接，例如 `#pinboard`、
  `#bilibili`、`#梦`、`#暴论`、`#网易云音乐`。使用正则表达式提取并分类。
- **pubDate 使用 GMT（RFC 2822）**：必须严格按日期范围过滤，只保留 pubDate 位于确认
  起止日期内的条目。处理 3/1～3/15 等历史范围时尤其重要，因为订阅源可能包含范围外的
  最新内容。加入条目前必须解析并比较日期。
- **内容类型不固定**：包括收藏文章、视频分享、个人想法、梦境记录、音乐分享、ACG
  内容、技术观察和生活动态。

使用脚本严格过滤：

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

尽可能按 hashtag 分类：

```markdown
#### 文章分享 (#pinboard)
- [Article title](url) - user's comment

#### 随想 (#暴论)
- 3/15: "some thought..."

#### 其他
- 3/12: 新电脑到了
```

### 2e：Apple Calendar 日程

使用 `icalBuddy` 查询日期范围内的日程：

```bash
icalBuddy -sd -ic "Personal,Learn&Create" \
  eventsFrom:{start_date} to:{end_date}
```

关键参数：

- `-sd`：按日期分组。
- `-ic "Personal,Learn&Create"`：只包含个人日历，跳过 `Work` 和
  `Scheduled Reminders`；提醒事项由 reminders-cli 单独收集。
- 输出包含日程摘要、日历名称、时间范围和备注。

输出已经按日期分组。保留聚会、预约、旅行和爱好等个人日程，跳过重复的工作会议。

使用 `icalBuddy calendars` 列出可用日历名称。

### 2f：Apple 提醒事项

查询当前提醒事项，了解用户正在关注和计划的内容：

```bash
reminders show-all
```

该命令返回所有列表中尚未完成的提醒事项，包括截止日期和备注。对于月记，当前提醒比
已完成提醒更有价值，可以反映生活目标、人际维护、重复习惯、后续计划和学习节点。

只保留「生活」「健康」「人际关系」「阅读」「提醒」等个人列表，跳过纯工作事项，例如
`sunlite: switch API`。

### 2g：RSS 每日摘要

读取 `~/code/ai-dev/repos/rss-agent/output/daily/` 中由 AI 筛选的每日摘要。

读取日期范围内存在的 `YYYY-MM-DD.md`。每份摘要包含：

- 带中文摘要的 AI 评分文章，分数为 0～100。
- 「核心推荐」4 篇和「开拓视野」3 篇。
- 每篇文章的标题、来源、分数、理由、分类和个人相关度。

提取分数不低于 70 的文章，作为本期阅读精选。按 URL 与 Pinboard 书签和 Telegram
频道分享去重；相同 URL 只保留一条。

### 2h：plrom Git 差异

plrom 仓库 `~/code/nini-dev/repos/plrom/` 是独立 Git 仓库，记录用户关注的
「人 × 社区 × 物」，并通过 GitHub Actions 自动同步到博客。

检查周期内的变更：

```bash
cd ~/code/nini-dev/repos/plrom
git log --since="{start_date}" --until="{end_date}" --oneline
# If there are commits, get the diff
FIRST_COMMIT=$(git log --since="{start_date}" --format="%H" --reverse | head -1)
if [ -n "$FIRST_COMMIT" ]; then
  git diff "$FIRST_COMMIT"^..HEAD -- README.md
fi
```

存在变更时，整理新增和移除内容：

- 新关注的人，例如技术博主、漫画家和 UP 主。
- 新加入的社区。
- 新发现的工具、产品或游戏。
- 已移除或移入弃坑列表的项目。

plrom 页面包含「人（技术博主、作家、漫画家、导演、UP 主、TG 芳邻、播客、歌手、
淘宝店主）」「组织或社区」「物（软件、硬件、游戏）」三个部分，用于记录兴趣变化和发现。

## 步骤 3：按模板整理

数据收集完成后，将素材整理到步骤 1 创建的骨架文件中。

### 整理规则

1. **生活事件**：合并日记、Calendar 日程和已完成提醒，按时间顺序形成叙述骨架。
   旅行连续数日等相关事件应归为一组。

2. **作品表格**：合并豆瓣条目和日记 TIL 中提到的作品，按标题去重，并尽量保留用户原话。

3. **文章章节**：合并 Pinboard 书签、RSS 摘要精选和 Telegram 分享，按 URL 去重。
   优先保留包含用户描述的 Pinboard 条目，格式沿用历史周记：

   ```markdown
   - [标题](url) - 用户的一句话评论或 AI 摘要
   ```

4. **plrom diff**：作为「新发现」小节展示新增内容。

5. **照片**：收集日记中的 `![[image]]` 和 `![](url)` 引用，连同上下文列出，供用户选择。

### 禁止事项

- 不代写周记正文，只整理原始材料。
- 不按 agent 判断过滤「不重要」的事件，重要性由用户决定。
- 合并不同日期的事件时，必须保留各自日期。
- 不包含正式工作周报内容，该内容属于 weekly-report。

## 步骤 4：展示并确认

展示收集结果摘要：

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

已写入文件：Areas/生活(Life)/月记(Monthly)/202603-title.md
你可以在 Obsidian 中打开这个文件，在素材基础上写你的周记。
```

询问是否需要：

- 调整时间范围并重新收集。
- 删除部分章节。
- 补充刚想起的手工记录。

将确认后的结构化素材写入文件。

## 数据源降级

| 不可用的数据源 | 处理方式 |
|---|---|
| 部分日期缺少日记 | 使用已有日期，并标记缺口 |
| 未设置 Pinboard token | 跳过，并标记「Pinboard 数据未获取」 |
| 豆瓣订阅源为空或被阻止 | 尝试 RSSHub；仍为空时保留表格供手工填写 |
| Telegram RSS 无法访问 | 跳过并标记 |
| Calendar 访问被拒绝 | 用 `icalBuddy calendars` 测试，并建议运行 `tccutil reset Calendar` |
| 缺少 rss-agent 输出 | 跳过，并标记「RSS 精选未找到」 |
| 未找到 plrom 仓库 | 跳过 plrom diff |

## 常见问题

| 问题 | 处理方式 |
|-------|-----|
| 豆瓣 RSS 为空 | 豆瓣可能阻止直接 RSS，改用 `https://rsshub.app/douban/people/niracler/interests` |
| icalBuddy 日历名称不匹配 | 运行 `icalBuddy calendars` 获取准确名称，并调整 `-ic` 过滤条件 |
| Pinboard 结果过多 | 增加标签过滤或提高 `fromdt` 精度 |
| plrom 在周期内没有 commit | 属于正常情况，plrom 更新频率较低 |
| Telegram RSS 没有日期过滤 | 获取全部条目，再按 pubDate 过滤日期范围 |
| 文件已经存在 | 询问覆盖、追加或改用其他名称 |
| 周记与月记输出路径不同 | 用户可能使用 `月记(Monthly)/`，询问或采用用户直接指定的路径 |
