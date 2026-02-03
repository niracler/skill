---
name: yunxiao
description: Use when working with Alibaba Cloud DevOps (Yunxiao/云效) or codeup.aliyun.com remotes. Triggers on「创建 MR」「提交评审」「推送代码」「更新任务」「查看任务」「发布版本」「打 tag」「云效」「yunxiao」
---

# 云效 CLI

阿里云云效 DevOps 命令行工具。记录了云效 API 的非显而易见的陷阱和必填字段规则，帮助一次调用成功。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| yunxiao MCP | mcp | No | Configure MCP server (preferred over CLI) |
| aliyun CLI | cli | No | `brew install aliyun-cli` then configure Access Key |
| git | cli | Yes | `brew install git` or [git-scm.com](https://git-scm.com/) |
| jq | cli | No | `brew install jq` (for JSON parsing in CLI mode) |

> At least one of yunxiao MCP or aliyun CLI is required. MCP is preferred.

## When to Use

- **创建/管理 MR**：在 codeup.aliyun.com 仓库上创建合并请求、更新描述、查看列表
- **任务管理**：查询/创建/更新任务状态、添加评论
- **发布管理**：通过云效 API 创建 Tag

## 工具选择

| 条件 | 推荐方式 |
|------|----------|
| MCP 服务已连接（`mcp__yunxiao__*` 工具可用） | **优先使用 MCP 工具**（包括 MR 操作） |
| 无 MCP 服务 | 使用 `aliyun` CLI |
| MCP 工具无覆盖的操作（更新 MR、编辑评论等） | 使用 `aliyun` CLI |

> ⚠️ `aliyun devops ListRepositories` 已知存在 `SYSTEM_UNAUTHORIZED_ERROR` 问题，获取仓库 ID 优先用 MCP 工具。

### 常用操作对应

| 任务 | MCP 工具 | CLI 替代 |
|------|----------|----------|
| 查询仓库 | `mcp__yunxiao__list_repositories` | `aliyun devops ListRepositories`（可能报权限错误） |
| 创建 MR | `mcp__yunxiao__create_change_request` | `aliyun devops CreateMergeRequest` |
| 查看 MR | `mcp__yunxiao__get_change_request` | `aliyun devops GetMergeRequest` |
| 更新 MR | — | `aliyun devops UpdateMergeRequest` |
| 查询任务 | `mcp__yunxiao__search_workitems` | `aliyun devops ListWorkitems` |
| 获取任务详情 | `mcp__yunxiao__get_work_item` | — |
| 更新任务状态 | `mcp__yunxiao__update_work_item` | REST API（见 openapi.md） |
| 查询工作流 | `mcp__yunxiao__get_work_item_workflow` | `aliyun devops ListWorkItemWorkFlowStatus` |
| 添加评论 | `mcp__yunxiao__create_work_item_comment` | REST API（见 openapi.md） |
| 编辑评论 | — | `aliyun devops UpdateWorkitemComment` |
| 查询字段配置 | `mcp__yunxiao__get_work_item_type_field_config` | `aliyun devops ListWorkItemAllFields` |
| 创建 Tag | — | `aliyun devops CreateTag` |

## Top 5 陷阱

最常踩的坑，完整规则见 [cheatsheet.md](references/cheatsheet.md)：

1. **仓库 ID 字段是 `Id`（大写 I）** — `jq` 用 `.id` 会返回 `null`
2. **创建 MR 必须提供** `sourceProjectId`、`targetProjectId`、`createFrom: "WEB"`
3. **更新任务状态必须用 REST API** — `aliyun devops POST /organization/.../workitems/updateWorkitemField`
4. **`updateWorkitemPropertyRequest` 必须是数组** `[{...}]`，字段名用 `fieldIdentifier`/`fieldValue`
5. **创建任务前必须查询必填字段** — 不同项目有不同的自定义必填字段

## 详细指南

- **AI 助手必读:** [cheatsheet.md](references/cheatsheet.md) — 13 条黄金法则 + 完整错误速查表
- **API 完整参考:** [openapi.md](references/openapi.md) — 配置指南、所有 API 操作模板、MR/任务/发布完整工作流
