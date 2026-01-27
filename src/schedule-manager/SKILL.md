---
name: schedule-manager
description: 通过 osascript 和 icalBuddy 管理 Apple Calendar 和 Reminders，遵循 GTD 方法论。触发场景：用户说「安排会议」「创建提醒」「查看日程」「规划下周」「添加待办」「今天要做什么」「周回顾」「记一下」「别忘了」时触发。
---

# Schedule Manager

通过 osascript 管理 Apple Calendar 和 Reminders，遵循 GTD 方法论。

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

### 查看日历列表

```bash
osascript -e 'tell application "Calendar" to get name of calendars'
```

### 查看今日/本周事件

**推荐使用 icalBuddy（更好的重复事件支持）：**

```bash
# 查看今日事件
icalBuddy -f eventsToday

# 查看本周事件
icalBuddy eventsFrom:today to:"+7d"

# 指定日历
icalBuddy -ic "工作" eventsToday
```

详见 [icalbuddy-guide.md](references/icalbuddy-guide.md)。

**备选方案（纯 osascript）：** 见 [osascript-calendar.md](references/osascript-calendar.md)。

### 创建事件

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        set startDate to (current date) + (1 * days)
        set hours of startDate to 14
        set minutes of startDate to 0
        set endDate to startDate + (1 * hours)
        make new event with properties {summary:"会议标题", start date:startDate, end date:endDate}
    end tell
end tell'
```

**可用属性：** `summary`, `start date`, `end date`, `description`, `location`, `allday event`

详见 [osascript-calendar.md](references/osascript-calendar.md)。

### 删除事件

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        delete (every event whose summary is "要删除的事件名")
    end tell
end tell'
```

## Reminders 操作

### 查看提醒列表

```bash
osascript -e 'tell application "Reminders" to get name of lists'
```

### 查看待办事项

```bash
osascript -e '
tell application "Reminders"
    set todoList to {}
    repeat with reminderList in lists
        set incompleteReminders to (reminders of reminderList whose completed is false)
        repeat with r in incompleteReminders
            set end of todoList to {name of r, name of reminderList}
        end repeat
    end repeat
    return todoList
end tell'
```

### 创建提醒

```bash
osascript -e '
tell application "Reminders"
    tell list "收件箱"
        make new reminder with properties {name:"任务名称", body:"任务描述", priority:1}
    end tell
end tell'
```

**可用属性：** `name`, `body`, `due date`, `allday due date`, `remind me date`, `priority`(0=无, 1=高, 5=中, 9=低), `completed`

详见 [osascript-reminders.md](references/osascript-reminders.md)。

### 完成提醒

```bash
osascript -e '
tell application "Reminders"
    tell list "收件箱"
        set completed of (first reminder whose name is "任务名称") to true
    end tell
end tell'
```

## 常见工作流

### 场景 1: 快速收集（GTD Capture）

用户说「记一下」「待会做」「别忘了」→ 创建 Reminder 到收件箱

```bash
osascript -e 'tell application "Reminders" to tell list "收件箱" to make new reminder with properties {name:"<任务名>"}'
```

### 场景 2: 安排会议

用户说「安排明天下午 2 点的会议」→ 创建 Calendar 事件

### 场景 3: 每日规划

1. 查看今日 Calendar 事件（`icalBuddy eventsToday`）
2. 查看 Reminders 待办
3. 为重要任务安排 Time Block（Calendar 事件）

### 场景 4: 周回顾（GTD Weekly Review）

1. 查看本周完成的提醒
2. 查看下周 Calendar 事件（`icalBuddy eventsFrom:today to:"+7d"`）
3. 整理 Reminders 列表

详见 [gtd-methodology.md](references/gtd-methodology.md)。

## 依赖与权限

### 依赖

- **icalBuddy**（推荐）：`brew install ical-buddy`

### 权限配置

首次运行需要授权：

1. 系统设置 → 隐私与安全性 → 日历 → 允许终端/Claude
2. 系统设置 → 隐私与安全性 → 提醒事项 → 允许终端/Claude

检查权限：

```bash
osascript -e 'tell application "Calendar" to get name of first calendar' 2>&1
osascript -e 'tell application "Reminders" to get name of first list' 2>&1
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `AppleEvent timed out` | 权限未授予 | 在系统设置中授权 |
| `Can't get list` | 列表不存在 | 先查看可用列表 |
| `Invalid date` | 日期格式错误 | 使用 `current date` 作为基准 |
| `icalBuddy: command not found` | 未安装 | `brew install ical-buddy` |
