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

## 关联 Skill

```yaml
# 日记流程中调用的 skill
related_skills:
  - schedule-manager  # 任务回顾 + 创建后续计划
  - anki-card-generator  # 生成记忆卡片
  # 注意：日记存储在 Obsidian，不需要 git 提交
```

## 写作风格（可选）

可选段。diary-note / diary-assistant 在追加日记内容时，会把这里的偏好叠加在 skill
的普遍规则（言简意赅、避免 narrator 腔、prose 不带 sub-heading）之上。

如果不写这段，走 skill 的普遍规则即可。

示例（按个人偏好修改或删除）：

```yaml
# 视觉与排版
bold_as_tldr: true              # 加粗关键短语作 visual TLDR（每 1-2 段一次）
section_divider: "--"           # 段内分隔符，避免再嵌一层 markdown sub-heading
quote_style: "「」"             # 中文角引号 vs 直引号
em_dash: false                  # 不用 ——、— 作分句符；改用逗号/分号/句号/括号

# 语气
parenthetical_asides: true      # 允许（筋疲力尽）这类括号补充
self_deprecating_close: true    # 自嘲式收尾
register: "工程师口语，不翻译腔"
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
