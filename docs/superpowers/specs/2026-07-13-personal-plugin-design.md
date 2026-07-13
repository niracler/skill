# Personal Plugin 拆分设计

## 背景

当前仓库通过多个 plugin 分发不同类别的 skill。`personal-knowledge` 同时包含两类内容：

- 可以由其他开发者配置后使用的通用个人效率工具。
- 依赖作者本地目录、Obsidian 结构、写作偏好和日记习惯的个人工作流。

普通使用者安装 `personal-knowledge` 时，不应同时安装一组只能适配作者个人环境的 skill。仓库需要增加独立的 `personal` plugin，把作者专用工作流从默认推荐安装集合中移出，同时保留作者自己的安装入口。

## 目标

- 新增 `personal` plugin，集中维护作者专用工作流。
- 普通使用者按 README 的推荐命令安装时，不会安装 `personal`。
- 保留 `personal` 的独立安装能力。
- 将迁入 `personal` 的 `SKILL.md` 改为中文，包括 frontmatter 中的触发说明和正文指令。
- 保持现有 skill 名称不变，避免破坏显式调用和已有配置。
- 保持现有用户配置路径和脚本接口不变。

## 非目标

- 不将 `personal` 移到独立仓库。
- 不把 `personal` 变成私有内容或权限受限内容。
- 不重写现有工作流逻辑。
- 不强制翻译脚本、命令、路径、配置键和代码标识符。
- 不修改 README 中已经存在但尚未提交的用户改动。

## Plugin 结构

新增以下目录：

```text
plugins/personal/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    ├── biweekly-collector/
    ├── diary-assistant/
    ├── diary-note/
    ├── note-to-blog/
    ├── weekly-report/
    └── writing-assistant/
```

Plugin 名称使用 `personal`。在当前 Marketplace 中，完整安装标识为 `personal@niracler-skills`，不需要在名称中重复作者信息。

## Skill 迁移范围

| Skill | 当前位置 | 迁移后位置 | 原因 |
| --- | --- | --- | --- |
| `diary-assistant` | `personal-knowledge` | `personal` | 依赖作者的 Obsidian 日记目录和日记结构 |
| `diary-note` | `personal-knowledge` | `personal` | 依赖共享日记配置和个人写作偏好 |
| `biweekly-collector` | `personal-knowledge` | `personal` | 依赖作者使用的数据源、目录和周记模板 |
| `note-to-blog` | `personal-knowledge` | `personal` | 依赖作者的 Obsidian、博客仓库和会话路径 |
| `writing-assistant` | `personal-knowledge` | `personal` | 包含作者个人写作风格和内容偏好 |
| `weekly-report` | `developer-workflows` | `personal` | 依赖作者的代码目录、Obsidian 日记和提醒事项结构 |

以下 skill 保留在 `personal-knowledge`：

- `schedule-manager`
- `pinboard-manager`
- `anki-card-generator`

这些 skill 仍然需要本地应用、账号或配置，但工作流本身可以由其他使用者配置后复用。

## 语言规则

迁入 `personal` 的每个 `SKILL.md` 遵循以下规则：

- `description` 使用中文说明触发条件、适用范围和排除范围。
- 标题、工作流、注意事项、错误处理和交互文案使用中文。
- skill 名称、文件名、命令、路径、环境变量、配置键和代码标识符保持原样。
- 必要的英文触发词可以保留在 `description` 中，但中文触发条件应作为主要内容。
- references 和 scripts 不做无关的整批翻译；仅在其内容直接影响中文工作流一致性时调整。

## 分发与安装

仓库级 Codex Marketplace 增加 `personal` 条目，使作者可以单独安装：

```bash
codex plugin add personal@niracler-skills
```

README 的普通安装命令不加入该命令。新增独立的 `Author-only plugin` 小节记录该命令和依赖，且不与通用 plugin 的推荐安装命令并列。

Claude Marketplace 同步增加 `personal` plugin 定义，避免两个 Marketplace 与实际目录结构不一致。README 不恢复已被用户删除的 Claude Marketplace 安装段落。

## 依赖关系

拆分后允许保留以下跨 plugin 关系：

- `diary-assistant` 继续依赖 `schedule-manager`，因此使用完整日记流程时需要安装 `personal-knowledge`。
- `writing-assistant` 可以继续选择性使用 `developer-workflows` 中的 `markdown-lint`。
- `note-to-blog` 与其他迁入的写作类 skill 仍位于同一 `personal` plugin 内。

README 的依赖说明需要反映这些关系，但不要求普通使用者安装 `personal`。

## 清单与文档更新

实现时需要同步更新：

- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- `plugins/personal/.codex-plugin/plugin.json`
- `plugins/personal-knowledge/.codex-plugin/plugin.json`
- `plugins/developer-workflows/.codex-plugin/plugin.json`
- README 中的 plugin 和 skill 清单
- CHANGELOG 中的拆分说明
- 依赖旧目录或固定 skill 数量的测试

不得覆盖 README 中与本次拆分无关的未提交改动。

## 验证

实现完成后运行以下检查：

```bash
bash scripts/validate.sh
npx skills add . --list --full-depth
```

并执行以下人工检查：

- `personal` manifest 只包含确认迁移的 6 个 skill。
- `personal-knowledge` 只保留 3 个通用 skill。
- `developer-workflows` 不再包含 `weekly-report`。
- Marketplace 中不存在重复 plugin 或失效路径。
- README 的普通安装命令不包含 `personal`。
- 旧目录中不存在迁移 skill 的残留副本。
- 每个迁入 skill 的 `SKILL.md` 以中文为主要指令语言。

## 风险与处理

### 跨 plugin 依赖不明显

`diary-assistant` 仍需要 `schedule-manager`。在 `personal` 的 manifest 描述和 README 作者自用说明中明确列出该依赖，避免只安装 `personal` 后才发现缺少能力。

### 迁移后引用旧路径

脚本和 references 多数使用相对路径，目录整体迁移后应继续有效。实现时使用全文搜索检查旧的 plugin 路径，并通过完整验证脚本确认不存在失效引用。

### 翻译改变机器可读内容

翻译仅覆盖自然语言指令。代码块、命令参数、配置键、环境变量和路径保持原样，防止中文化过程改变运行行为。
