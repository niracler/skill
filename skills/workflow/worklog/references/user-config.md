# 身份自动获取

worklog skill 在运行时自动获取用户身份，无需手动配置。

## 获取来源

| 数据项 | 获取方式 | 用途 |
|--------|---------|------|
| git author | `git config user.name` | stats.sh 本地 commit 过滤 |
| GitHub username | `gh api user --jq '.login'` | github.sh PR/Issue 查询 |
| 云效用户 | `get_current_user` MCP 工具 | MR/Bug/Task 查询 |
| 云效组织 ID | `get_current_organization_info` MCP 工具 | 组织范围查询 |

## 前提条件

- **本地 git 统计** — 无额外要求（使用本地 git config）
- **GitHub 数据** — 需要 `gh` CLI 已认证（`gh auth login`）
- **云效数据** — 需要云效 MCP server 已连接
