# icalBuddy 命令参考

icalBuddy 是一个命令行工具，用于查询 macOS 日历事件和提醒，对重复事件的支持比 osascript 更可靠。

## 安装

```bash
brew install ical-buddy
```

## 基础命令

### 查看今日事件

```bash
icalBuddy eventsToday
```

### 查看今日 + 明日事件

```bash
icalBuddy eventsToday+1
```

### 查看本周事件

```bash
icalBuddy eventsFrom:today to:"+7d"
```

### 查看指定日期范围

```bash
# 从今天到月底
icalBuddy eventsFrom:today to:"end of month"

# 指定具体日期
icalBuddy eventsFrom:"2024-01-15" to:"2024-01-31"
```

### 查看未完成提醒

```bash
icalBuddy uncompletedTasks
```

### 查看今日到期的任务

```bash
icalBuddy tasksDueBefore:today+1
```

## 日历筛选

### 只看指定日历

```bash
# 单个日历
icalBuddy -ic "工作" eventsToday

# 多个日历
icalBuddy -ic "工作" -ic "个人" eventsToday
```

### 排除指定日历

```bash
icalBuddy -ec "节假日" eventsToday
```

### 列出所有日历

```bash
icalBuddy calendars
```

## 输出格式

### 简洁输出

```bash
icalBuddy -f eventsToday
```

### 自定义分隔符

```bash
icalBuddy -ss " | " eventsToday
```

### 显示时间格式

```bash
# 24小时制
icalBuddy -tf "%H:%M" eventsToday

# 12小时制
icalBuddy -tf "%I:%M %p" eventsToday
```

### 日期格式

```bash
icalBuddy -df "%Y-%m-%d" eventsFrom:today to:"+7d"
```

### 不显示日历名称

```bash
icalBuddy -nc eventsToday
```

### 不显示位置

```bash
icalBuddy -nrd eventsToday
```

### 按日历分组（默认）

```bash
icalBuddy -sc eventsToday
```

### 按日期分组

```bash
icalBuddy -sd eventsFrom:today to:"+7d"
```

## 输出属性控制

### 只显示标题和时间

```bash
icalBuddy -eep "url,location,notes" eventsToday
```

### 包含所有属性

```bash
icalBuddy -iep "*" eventsToday
```

### 可用属性

- `title` - 事件标题
- `datetime` - 日期时间
- `location` - 地点
- `notes` - 备注
- `url` - 链接
- `attendees` - 参与者
- `priority` - 优先级

## 提醒操作

### 查看所有未完成提醒

```bash
icalBuddy uncompletedTasks
```

### 查看指定列表的提醒

```bash
icalBuddy -ic "工作" uncompletedTasks
```

### 查看今日到期的任务

```bash
icalBuddy tasksDueBefore:today+1
```

### 查看本周到期的任务

```bash
icalBuddy tasksDueBefore:"+7d"
```

## 常用组合

### 每日规划视图

```bash
echo "=== 今日事件 ===" && icalBuddy -f eventsToday && echo "" && echo "=== 待办事项 ===" && icalBuddy uncompletedTasks
```

### 周规划视图

```bash
icalBuddy -sd eventsFrom:today to:"+7d"
```

### 工作日历专用

```bash
icalBuddy -ic "工作" -f eventsToday+7
```

## 与 osascript 对比

| 功能 | icalBuddy | osascript |
|------|-----------|-----------|
| 查询速度 | 快 | 较慢 |
| 重复事件 | 完整支持 | 支持有限 |
| 创建事件 | 不支持 | 支持 |
| 修改事件 | 不支持 | 支持 |
| 删除事件 | 不支持 | 支持 |
| 安装依赖 | 需要 brew | 系统内置 |

**建议**：

- **查询操作** → 使用 icalBuddy
- **创建/修改/删除操作** → 使用 osascript

## 常见问题

### 中文显示乱码

```bash
icalBuddy -nc eventsToday
```

### 权限问题

确保终端有日历访问权限：系统设置 → 隐私与安全性 → 日历

### 时区问题

```bash
# 强制使用本地时区
TZ=Asia/Shanghai icalBuddy eventsToday
```

## 更多帮助

```bash
# 查看完整帮助
icalBuddy --help

# 查看版本
icalBuddy --version
```
