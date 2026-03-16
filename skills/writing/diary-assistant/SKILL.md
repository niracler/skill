---
name: diary-assistant
metadata: {"openclaw":{"emoji":"📔","requires":{"bins":["osascript","reminders-cli"],"skills":["schedule-manager"]}}}
description: >-
  (macOS, requires schedule-manager) Use this skill whenever the user wants to write
  a personal diary entry or daily journal — this includes any request to record today's
  events, write a diary, log what happened today, or capture personal reflections.
  Invoke immediately for phrases like 帮我写日记, 写日记, 记录今天, 今天的日记,
  "write my diary", or "daily log". This skill guides a complete journaling session:
  reviewing today's tasks from Reminders, reflective guided questions, composing the
  entry, and scheduling follow-up plans. Distinct from diary-note (quick append) and
  weekly-report (work summary).
---

# Diary Assistant

日记写作助手，提供完整的日记工作流，包含任务回顾、启发提问和任务捕获。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| macOS | system | Yes | This skill requires macOS |
| reminders-cli | cli | Yes | `brew install keith/formulae/reminders-cli` |
| schedule-manager | skill | Yes | Included in `npx skills add niracler/skill` |
| anki-card-generator | skill | No | Included in `npx skills add niracler/skill` |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## 核心原则

| 原则 | 说明 |
|------|------|
| **45 分钟约束** | 完整流程控制在一个番茄钟内完成 |
| **GTD 集成** | 开始时回顾今日任务，结束时捕获新计划 |
| **启发而非代写** | 用提问引导思考，不替用户决定内容 |

## 完整流程

```text
┌──────────────────────────────────────────────────────────┐
│       diary-assistant 完整流程（目标 ≤35min）              │
└──────────────────────────────────────────────────────────┘

  ┌──────────────┐
  │ 用户触发日记  │
  └──────┬───────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 1. Pre-Diary Clarification  (~1min) │
  │    确认日期：2026-01-29.md         │
  └──────┬─────────────────────────────┘
         │
         ▼
    ┌────┴──────────┐
    │ 日记文件已存在？ │
    └────┬──────────┘
      是 │         │ 否
         ▼         │
  ┌─────────────┐  │
  │ 选择模式：   │  │
  │ 继续/追加/  │  │
  │ 重新开始    │  │
  └──────┬──────┘  │
         └────┬────┘
              ▼
  ┌────────────────────────────────────┐
  │ 2. 今日任务回顾（简化）    (~2min)   │
  │    获取 Reminders → 批量确认       │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 3. 启发提问              (~20min)   │
  │                                    │
  │    Q1「今天有什么想记录的？」       │
  │    Q2「有什么收获或感受？」         │
  │    Q3「之后有什么计划？」           │
  │                                    │
  │    → 计划直接解析为 Reminders       │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 4. 整理成文              (~10min)   │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 5. 智能收尾              (~0-5min)  │
  │    检测到 TIL → 「要生成 Anki 吗？」│
  └──────┬─────────────────────────────┘
         │
         ▼
      ┌──────┐
      │ 完成  │  总计 ~33-38min
      └──────┘
```

## 1. Pre-Diary Clarification

开始前确认日期和文件：

```text
Claude: 「今天的日记是 2026-01-29.md 吗？」
用户: 「是」/ 「不是，是昨天的」
```

### 文件已存在处理

如果文件已存在，提供选项：

| 选项 | 说明 |
|------|------|
| **继续** | 在现有内容基础上继续编辑 |
| **追加** | 在文件末尾添加新内容 |
| **重新开始** | 清空重写（会确认） |

## 2. 今日任务回顾

调用 `schedule-manager` 获取今日 Reminders，然后批量确认：

```text
今日计划的 5 件事：
1. 写文档
2. 修 bug
3. 开会
4. 回复邮件
5. 复习英语

哪些完成了？（输入序号，如「1,3」，或「全部」/「都没完成」）
```

**处理逻辑：**

- 用户说「1,3」→ 标记 1、3 为完成，追问「2、4、5 延期到什么时候？」
- 用户说「全部」→ 全部标记完成
- 用户说「都没完成」→ 追问「延期到什么时候？」

**延期时间解析：**

- 「明天」→ tomorrow
- 「后天」→ 2 days
- 「周五」→ friday
- 「下周」→ next monday

**无任务时跳过此步骤。**

### 命令参考

```bash
# 获取今日任务
reminders show-all --due-date today

# 完成任务
reminders complete "<列表名>" <index>

# 延期到指定日期（删除后重建）
reminders delete "<列表名>" <index>
reminders add "<列表名>" "<任务名>" --due-date "<用户指定的日期>"
```

## 3. 启发提问

| 顺序 | 问题 |
|------|------|
| Q1 | 「今天有什么想记录的？」 |
| Q2 | 「有什么收获或感受？」 |
| Q3 | 「之后有什么计划？」 |

### 提问节奏

```text
Claude: 「今天有什么想记录的？」
用户: [回答]
Claude: [确认/追问] → 「好的，下一个问题：有什么收获或感受？」
```

## 4. 任务捕获

最后一个问题「之后有什么计划？」的回答会自动解析为任务：

### 日期解析示例

| 用户输入 | 解析结果 |
|----------|----------|
| 「明天要交报告」 | 明天 |
| 「周五开会」 | 本周五 |
| 「下周一复习」 | 下周一 |
| 「月底前提交」 | 本月最后一天 |
| 「下个月初」 | 下月 1 号 |

### 确认后创建

```text
Claude: 「检测到以下计划，确认创建到 Reminders 吗？」
  - 明天：交报告
  - 周五：开会

用户: 「好」

Claude: [调用 schedule-manager 创建]
```

```bash
reminders add "提醒" "交报告" --due-date "tomorrow"
reminders add "提醒" "开会" --due-date "friday"
```

## 5. 智能收尾

根据日记内容推荐后续操作：

| 检测内容 | 推荐操作 |
|----------|----------|
| TIL（今天学到的东西） | 「检测到你今天学了新东西，要生成 Anki 卡片吗？」→ 调用 `anki-card-generator` |

**注意：** 日记存储在 Obsidian（iCloud 同步），不需要 git 提交。

## 时间预算

| 步骤 | 时间 |
|------|------|
| 确认日期 + 文件处理 | ~1 min |
| 任务回顾 | ~2 min |
| 启发提问（含计划） | ~20 min |
| 整理成文 | ~10 min |
| 智能收尾（可选） | ~0-5 min |
| **总计** | **~33-38 min** |

## 用户配置

见 [user-config.md](references/user-config.md) 配置日记路径和工作仓库。
