# Codex 自动代码审查设计

## 背景

仓库当前包含 3 个 GitHub Actions workflow：Claude 自动代码审查、`@claude` 交互入口和 ClawHub 发布。现有 workflow 将全部删除，后续 CI 能力按实际需要重新建立。

代码审查改用 Codex 官方 GitHub 集成，不通过仓库内的 GitHub Actions workflow 运行。该集成由 Codex 云端管理，可对每个新建并进入待审状态的 PR 自动提交 GitHub Review。

## 目标

- 删除 `.github/workflows` 中的全部现有 workflow。
- 为当前 GitHub 仓库启用 Codex Code Review。
- 启用 Automatic reviews，使每个进入待审状态的 PR 自动触发 Codex Review。
- 通过仓库顶层 `AGENTS.md` 提供稳定、明确的审查规则。
- 不在仓库中保存 OpenAI API Key，也不创建 `openai/codex-action` workflow。

## 非目标

- 不恢复 ClawHub 发布流程。
- 不新增 lint、测试、构建或发布 workflow。
- 不使用 Codex GitHub Action 模拟官方 GitHub 集成。
- 不改动现有 Skill、插件 manifest 或 marketplace 数据。

## 实施设计

### 仓库变更

删除以下文件：

- `.github/workflows/claude-code-review.yml`
- `.github/workflows/claude.yml`
- `.github/workflows/publish-clawhub.yml`

新增顶层 `AGENTS.md`，其中的 `Review guidelines` 要求 Codex Review 重点检查：

- Skill 目录结构和 `SKILL.md` 的完整性。
- 文档链接、文件路径和命令示例是否有效。
- 插件 manifest 与 marketplace 配置是否一致。
- 是否意外提交密钥、令牌、个人数据或其他敏感信息。
- 行为变更是否同步更新相关文档。

### Codex 云端配置

在 Codex 设置中完成以下操作：

1. 确认当前仓库已连接到 Codex cloud。
2. 为当前仓库启用 Code review。
3. 启用 Automatic reviews。

该配置不产生仓库文件。若当前会话无法访问已登录的 Codex 设置页面，则保留为明确的人工配置步骤。

## 权限与安全

官方 GitHub 集成负责读取 PR diff 并提交标准 GitHub Review。仓库不新增 API Key、GitHub Secret 或可写 workflow 权限。顶层 `AGENTS.md` 只提供审查规则，不授予额外权限。

## 验证

- 确认 `.github/workflows` 下不存在 workflow 文件。
- 对新增的 `AGENTS.md` 进行 Markdown 格式检查。
- 检查 Git diff，确认没有删除 `.github` 下的其他配置。
- 在 Codex 设置中确认 Code review 与 Automatic reviews 均已启用。
- 创建或使用一个测试 PR，确认 Codex 自动提交 Review，无需评论 `@codex review`。

## 回退

如需停止自动审查，在 Codex 设置中关闭 Automatic reviews；如需彻底停用，再关闭该仓库的 Code review。仓库侧无需恢复 workflow。`AGENTS.md` 可继续作为 Codex 的仓库级指导文件保留。
