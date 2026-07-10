---
name: schedule-manager
metadata: {"openclaw":{"emoji":"📅","requires":{"bins":["osascript","reminders-cli"]}}}
description: >-
  (macOS only) Use this skill for ALL Apple Calendar and Reminders management tasks
  using osascript and reminders-cli, following GTD methodology. Invoke immediately
  when the user wants to: schedule a meeting or event, add a todo or reminder, check
  today's agenda, plan the week ahead, do a weekly review, or capture any task they
  don't want to forget. Also use when the user says 安排会议, 创建提醒, 查看日程,
  规划下周, 添加待办, 记一下, 别忘了, 今天要做什么, 周回顾. This is the right skill
  any time the user wants to interact with macOS Calendar or Reminders apps.
---

# Schedule Manager

通过 osascript (Calendar) 和 reminders-cli (Reminders) 管理日程，遵循 GTD 方法论。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| macOS | system | Yes | This skill requires macOS |
| osascript | cli | Yes | Built-in on macOS |
| reminders-cli | cli | Yes | `brew install keith/formulae/reminders-cli` |
| Schedule YAML | data | No | `~/code/*/planning/schedules/*.yaml` — for cross-project weekly planning |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

### 权限配置

首次运行需要授权，进入系统设置 → 隐私与安全性：

1. **日历** - 勾选 Terminal / iTerm / 你使用的终端应用
2. **提醒事项** - 同上

⚠️ 修改权限后需重启终端应用

## 核心原则（GTD 风格）

| 工具 | 用途 | 示例 |
|------|------|------|
| Calendar | 固定时间承诺 | 会议、约会、截止日期 |
| Reminders | 待办事项（无固定时间） | 购物清单、任务、想法 |

**决策流程：**

```text
有具体时间？ → Calendar 事件
无具体时间？ → Reminders 待办
需要提醒？ → 两者都可设置提醒
```

## 模式选择

| 用户意图 | 模式 | 操作 |
|----------|------|------|
| 「安排会议」「创建事件」 | Calendar | 创建带时间的事件 |
| 「添加待办」「创建提醒」「记一下」 | Reminders | 创建任务 |
| 「查看日程」「今天有什么」 | 查询 | 查询 Calendar + Reminders |
| 「规划下周」「周回顾」 | 规划 | 综合工作流 |

## Calendar 操作

通过 osascript 管理 Calendar 事件（查看、创建、删除）。

详见 [osascript-calendar.md](references/osascript-calendar.md) 获取完整命令模板。

## Reminders 操作

推荐使用 `reminders-cli`（osascript 访问 Reminders 非常慢）。

常用命令速查：

```bash
reminders show-lists              # 查看列表
reminders show-all --due-date today  # 今日待办
reminders add "列表" "任务"         # 创建
reminders complete "列表" 0        # 完成
```

详见 [reminders-cli-guide.md](references/reminders-cli-guide.md) 获取完整命令参考。
osascript 备选见 [osascript-reminders.md](references/osascript-reminders.md)。

## 常见工作流

### 场景 1: 快速收集（GTD Capture）

用户说「记一下」「待会做」「别忘了」→ 创建 Reminder 到收件箱

```bash
reminders add "提醒" "<任务名>"
```

### 场景 2: 安排会议

用户说「安排明天下午 2 点的会议」→ 创建 Calendar 事件（使用 osascript）

### 场景 3: 每日规划

1. 查看今日 Calendar 事件（osascript）
2. 查看 Reminders 待办（`reminders show-all`）
3. 为重要任务安排 Time Block（Calendar 事件）

### 场景 4: 周回顾（GTD Weekly Review）

1. 查看本周完成的提醒
2. 查看下周 Calendar 事件（osascript）
3. 整理 Reminders 列表（`reminders show-all`）

详见 [gtd-methodology.md](references/gtd-methodology.md)。

### 场景 5: 跨项目周规划（需要 Schedule YAML）

当 `~/code/*/planning/schedules/*.yaml` 存在时，「规划下周」工作流增加项目排期上下文：

1. 扫描 `~/code/*/planning/schedules/*.yaml`，解析每个文件的 `project`、`timeline`、`capacity`
2. 查看下周 Calendar 已有事件（osascript）
3. 查看 Reminders 待办（`reminders show-all`）
4. 从 schedule YAML 中提取下周相关 module（按 `weeks` 字段匹配）
5. 按 `capacity.days_per_week` 估算各项目时间分配
6. 合并展示：Calendar 事件 + Reminders 待办 + 各项目模块任务
7. 标注产能冲突（总分配 > 可用工作日）
8. 建议 Calendar time block（展示建议，用户确认后创建）

**无 Schedule YAML 时**：跳过步骤 4-7，退化为标准的场景 4 周回顾流程。

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `AppleEvent timed out` | 权限未授予 | 在系统设置中授权 |
| `Can't get list` | 列表不存在 | 先用 `reminders show-lists` 查看可用列表 |
| `Invalid date` | 日期格式错误 | 使用 `current date` 作为基准 |
| `reminders: command not found` | 未安装 | `brew install keith/formulae/reminders-cli` |
| osascript Reminders 卡顿 | 已知性能问题 | 改用 `reminders-cli` |
