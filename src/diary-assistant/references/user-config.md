# 用户配置

diary-assistant 的个人偏好配置。

## 日记配置

```yaml
# 日记文件路径（支持 ~ 展开）
diary_path: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/Archives/日记(Daily)/

# 日记文件命名模板（{date} 会替换为 YYYY-MM-DD）
diary_template: "{date}.md"

# 示例：2026-01-27 的日记路径
# → ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/Archives/日记(Daily)/2026-01-27.md
```

## 工作仓库配置

```yaml
# 本地 git 仓库目录（用于 Work Log 自动获取）
work_repos:
  - ~/code/azoulalite-dev/repos/azoulalite-backend
  - ~/code/nini-dev/repos/skill

# 云效组织 ID（如使用云效）
yunxiao_org_id: "623ea833581fc62661c91d9e"
```

## 关联 Skill

```yaml
# 收尾时可调用的 skill
related_skills:
  - schedule-manager  # 任务回顾 + 创建后续计划
  - anki-card-generator  # 生成记忆卡片
  # 注意：日记存储在 Obsidian，不需要 git 提交
```

## 如何使用

1. 将上述配置根据个人情况修改
2. AI 在日记模式启动时会尝试读取用户的日记文件
3. 如果路径不对，会询问用户确认

## 默认行为

如果没有配置：

- **日记路径** - 询问用户「今天的日记文件在哪里？」
- **Work Log** - 工作日自动获取（不询问），周末跳过
- **任务回顾** - 自动获取今日 Reminders 并批量确认完成情况
- **收尾** - 检测到 TIL 内容时询问是否生成 Anki 卡片
