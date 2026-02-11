# 云效 OpenAPI 参考

通过阿里云 CLI 程序化访问云效服务。

## 配置

### 第 1 步：安装依赖

```bash
# aliyun CLI（macOS）
brew install aliyun-cli

# 或从 GitHub 下载
# https://github.com/aliyun/aliyun-cli/releases
```

还需要 `jq` 用于解析 JSON 响应：

```bash
# macOS
brew install jq
# Ubuntu/Debian: sudo apt-get install jq
# Windows: winget install jqlang.jq (或 scoop install jq)
```

### 第 2 步：创建 AccessKey

**方案 A: RAM 用户（推荐，更安全）**

1. 前往 [RAM 控制台](https://ram.console.aliyun.com/users)
2. 创建 RAM 用户，启用"OpenAPI 访问"
3. 添加权限：`AliyunDevOpsFullAccess`
4. **重要:** 将 RAM 用户添加到云效组织：
   - 云效控制台 > 组织 > 成员 > 添加成员
   - 选择"RAM 用户"并添加

**方案 B: 主账户（快速但安全性较低）**

1. 前往 [AccessKey 管理](https://ram.console.aliyun.com/manage/ak)
2. 创建 AccessKey
3. 立即下载保存（Secret 只显示一次！）

### 第 3 步：配置 aliyun CLI

```bash
aliyun configure
# Access Key Id: [你的-access-key-id]
# Access Key Secret: [你的-access-key-secret]
# Default Region Id: cn-hangzhou
# Default Output Format: json
```

验证配置：

```bash
aliyun configure list
```

## ID 获取

大多数 API 都需要 organizationId、repositoryId 等 ID，首次使用前获取后可复用。

### 从 git remote 提取组织 ID

```bash
ORG_ID=$(git remote get-url origin | sed -E 's|.*codeup.aliyun.com[:/]([^/]+)/.*|\1|')
echo "组织 ID: $ORG_ID"
```

### 获取仓库 ID

**方式 1: MCP 工具（推荐）**

```python
mcp__yunxiao__list_repositories(organizationId="<org-id>", search="repo-name")
# 返回: [{ "id": 5997883, "name": "sunlite-backend", "path": "azoulalite-backend", ... }]
```

> ⚠️ 仓库改名后 `name` 变但 `path` 不变。`search` 匹配的是 path，需用当前名称搜索。

**方式 2: CLI（可能失败）**

```bash
# ⚠️ 此 API 已知可能报 SYSTEM_UNAUTHORIZED_ERROR，优先用 MCP
REPO_ID=$(aliyun devops ListRepositories --organizationId $ORG_ID \
  | jq -r ".result[] | select(.name == \"$REPO_NAME\") | .Id")
```

### 通过 API 查询

```bash
# 获取组织 ID（必须加 --minAccessLevel 5）
aliyun devops ListOrganizations --minAccessLevel 5 \
  | jq -r '.result[] | "\(.organizationId): \(.organizationName)"'

# 获取项目 ID
aliyun devops ListProjects --organizationId <org-id> --category Project \
  | jq -r '.projects[] | "\(.identifier): \(.name)"'

# 获取仓库 ID
aliyun devops ListRepositories --organizationId <org-id> \
  | jq -r '.result[] | "\(.Id): \(.name)"'

# 获取任务类型 ID
aliyun devops ListProjectWorkitemTypes \
  --organizationId <org-id> --projectId <project-id> \
  --category Task --spaceType Project \
  | jq -r '.workitemTypes[] | "\(.identifier): \(.name)"'

# 获取状态 ID 列表
aliyun devops ListWorkItemWorkFlowStatus \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --workitemTypeIdentifier <task-type-id> \
  --workitemCategoryIdentifier Task \
  | jq -r '.statuses[] | "\(.identifier): \(.name)"'

# 获取用户 accountId
aliyun devops ListOrganizationMembers --organizationId <org-id> \
  | jq -r '.members[] | "\(.accountId): \(.organizationMemberName)"'
```

**accessLevel 说明:**

- 5: 企业外部成员
- 15: 企业成员
- 60: 企业管理员
- 70: 企业拥有者

| ID | 如何获取 |
| --- | --- |
| organizationId | `ListOrganizations --minAccessLevel 5` 或从 git remote 提取 |
| repositoryId | MCP `list_repositories` 返回的 `id` 字段，或 CLI `ListRepositories` 的 `Id`（大写 I） |
| spaceIdentifier (项目ID) | `ListProjects` 返回的 `identifier` 字段 |
| accountId (用户ID) | `ListOrganizationMembers` 返回的 `accountId` 字段 |

## MR 操作

### 使用 MCP 创建 MR（推荐）

前置条件：分支已推送到远程。

```python
# 1. 获取仓库 ID
repos = mcp__yunxiao__list_repositories(organizationId="<org-id>", search="repo-name")
repo_id = repos[0]["id"]  # e.g. 5997883

# 2. 创建 MR
mcp__yunxiao__create_change_request(
    organizationId="<org-id>",
    repositoryId=str(repo_id),
    title="feat: your MR title",
    sourceBranch="feature/your-feature",
    targetBranch="main",
    sourceProjectId=repo_id,
    targetProjectId=repo_id,
    description="## Summary\n\n- Change 1\n- Change 2",
)
```

MCP 工具会自动填充 `createFrom: "WEB"`，无需手动指定。

### 使用 CLI 创建 MR

前置条件：分支已推送到远程，已获取仓库 ID（见「ID 获取」章节）。

### 创建合并请求（API 参考）

```bash
aliyun devops CreateMergeRequest \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --body '{
    "title": "feat: your title",
    "description": "Description here",
    "sourceBranch": "<your-branch>",
    "targetBranch": "main",
    "sourceProjectId": <repo-id>,
    "targetProjectId": <repo-id>,
    "createFrom": "WEB"
  }'
```

**必需参数（body 中）:**

| 参数 | 说明 |
|------|------|
| `title` | MR 标题 |
| `sourceBranch` | 源分支名 |
| `targetBranch` | 目标分支名 |
| `sourceProjectId` | 源仓库 ID（同 repositoryId） |
| `targetProjectId` | 目标仓库 ID（同 repositoryId） |
| `createFrom` | 必须为 `"WEB"` |

**可选参数:**

| 参数 | 说明 |
|------|------|
| `description` | MR 描述（支持 Markdown） |
| `reviewerIds` | 评审人 ID 列表 |
| `workItemIds` | 关联的工作项 ID |

**指定评审人示例:**

```bash
aliyun devops CreateMergeRequest \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --body '{
    "title": "feat: your title",
    "sourceBranch": "<your-branch>",
    "targetBranch": "main",
    "sourceProjectId": <repo-id>,
    "targetProjectId": <repo-id>,
    "createFrom": "WEB",
    "reviewerIds": ["<user-id-1>", "<user-id-2>"]
  }'
```

**关联工作项示例:**

```bash
aliyun devops CreateMergeRequest \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --body '{
    "title": "feat: your title",
    "sourceBranch": "<your-branch>",
    "targetBranch": "main",
    "sourceProjectId": <repo-id>,
    "targetProjectId": <repo-id>,
    "createFrom": "WEB",
    "workItemIds": ["<workitem-id>"]
  }'
```

### 更新 MR 描述

已创建的 MR 可以通过 `UpdateMergeRequest` 更新标题、描述等信息。

```bash
aliyun devops UpdateMergeRequest \
  --organizationId $ORG_ID \
  --repositoryId $REPO_ID \
  --localId <mr-local-id> \
  --body '{
    "title": "feat: updated title",
    "description": "## Summary\n\n- Updated description"
  }'
```

**参数说明：**

- `--localId`: MR 的本地编号（在 URL 中可见，如 `/mergerequests/56` 中的 `56`）
- `--body`: 要更新的字段，支持 `title`、`description` 等

**获取 MR localId：**

```bash
aliyun devops ListMergeRequests \
  --organizationId $ORG_ID \
  --repositoryId $REPO_ID \
  | jq -r '.result[] | "\(.localId): \(.title) [\(.state)]"'
```

### 列出合并请求

```bash
# 查询所有 MR
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --pageSize 50

# 按时间范围查询
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --createdBefore "2026-01-06T00:00:00Z" \
  --orderBy created_at \
  --pageSize 50
```

**常用参数:**

- `--createdBefore`: 起始创建时间 (ISO 8601 格式)
- `--createdAfter`: 截止创建时间
- `--authorIds`: 按创建人过滤
- `--orderBy`: 排序字段 (`created_at` 或 `updated_at`)
- `--page` / `--pageSize`: 分页参数

## 任务管理

### 列出任务

```bash
aliyun devops ListWorkitems \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --category Task \
  --maxResults 50
```

**category 可选值:**

- `Task`: 任务
- `Req`: 需求
- `Bug`: 缺陷
- `Risk`: 风险
- `Request`: 原始诉求

### 获取工作项类型

```bash
aliyun devops ListProjectWorkitemTypes \
  --organizationId <org-id> \
  --projectId <project-id> \
  --category Task \
  --spaceType Project
```

返回结果中的 `identifier` 即为 `workitemTypeIdentifier`。

### 获取工作项字段定义

创建任务前，必须获取项目的工作项字段定义（特别是必填字段）：

```bash
aliyun devops ListWorkItemAllFields \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --workitemTypeIdentifier <task-type-id>
```

筛选必填字段：

```bash
... | jq '.fields[] | select(.isRequired == true) | {identifier, name, format, options}'
```

### 创建任务

**⚠️ 创建前必须先查询必填字段配置（见上方"获取工作项字段定义"）。**

```bash
aliyun devops CreateWorkitem \
  --organizationId <org-id> \
  --body '{
    "subject": "任务标题",
    "description": "任务描述（支持 Markdown）",
    "space": "<project-id>",
    "spaceIdentifier": "<project-id>",
    "spaceType": "Project",
    "category": "Task",
    "workitemType": "<task-type-id>",
    "workitemTypeIdentifier": "<task-type-id>",
    "assignedTo": "<user-id>",
    "fieldValueList": [
      {"fieldIdentifier": "<custom-field-id>", "value": "<value>"},
      {"fieldIdentifier": "priority", "value": "<priority-identifier>"}
    ]
  }'
```

**必填参数（body 中）:**

| 参数 | 说明 |
|------|------|
| `subject` | 任务标题 |
| `space` | 项目 ID（与 spaceIdentifier 相同） |
| `spaceIdentifier` | 项目 ID（与 space 相同） |
| `spaceType` | 固定为 `"Project"` |
| `category` | 工作项大类：Task/Req/Bug/Risk |
| `workitemType` | 工作项类型 ID（与 workitemTypeIdentifier 相同） |
| `workitemTypeIdentifier` | 工作项类型 ID（与 workitemType 相同） |
| `assignedTo` | 负责人的阿里云账号 ID |
| `fieldValueList` | 自定义字段列表（项目配置的必填字段必须包含） |

**fieldValueList 格式:**

```json
{
  "fieldIdentifier": "字段标识符",
  "value": "字段值"
}
```

- 选项类字段（如 priority）：`value` 使用选项的 `identifier`，不是 `displayValue`
- 文本类字段：`value` 直接使用文本值

**⚠️ 常见陷阱:**

1. **字段重复**: `space`/`spaceIdentifier` 和 `workitemType`/`workitemTypeIdentifier` 必须同时提供，值相同
2. **自定义必填字段**: 项目管理员配置的必填字段必须在 fieldValueList 中提供，否则报错 `字段【xxx】不能为空`
3. **选项值格式**: priority 等选项字段需要用 identifier（如 `c31cc0589797babd16889232e4`），不是 displayValue（如 `中`）

### 获取工作流状态列表

更新任务状态前，需要获取可用的状态列表：

```bash
aliyun devops ListWorkItemWorkFlowStatus \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --workitemTypeIdentifier <task-type-id> \
  --workitemCategoryIdentifier Task
```

**必需参数:**

| 参数 | 说明 |
|------|------|
| `organizationId` | 组织 ID |
| `spaceIdentifier` | 项目 ID |
| `spaceType` | 固定为 `"Project"` |
| `workitemTypeIdentifier` | 工作项类型 ID |
| `workitemCategoryIdentifier` | 工作项大类：`Task`/`Req`/`Bug` |

**返回示例:**

```json
{
  "statuses": [
    {"identifier": "100005", "name": "待处理"},
    {"identifier": "100010", "name": "处理中"},
    {"identifier": "100014", "name": "已完成"}
  ]
}
```

### 更新任务状态

**⚠️ 必须使用 REST API 方式调用**（普通命令行参数方式不支持）：

```bash
aliyun devops POST /organization/<org-id>/workitems/updateWorkitemField \
  --body '{
    "workitemIdentifier": "<workitem-id>",
    "updateWorkitemPropertyRequest": [
      {"fieldIdentifier": "status", "fieldValue": "<status-id>"}
    ]
  }'
```

**body 参数:**

| 参数 | 说明 |
|------|------|
| `workitemIdentifier` | 工作项 ID |
| `updateWorkitemPropertyRequest` | **必须是数组**，包含要更新的字段 |
| `updateWorkitemPropertyRequest[].fieldIdentifier` | 字段标识符（如 `status`） |
| `updateWorkitemPropertyRequest[].fieldValue` | 字段值（如 `100014` 表示"已完成"） |

**⚠️ 常见陷阱:**

1. **必须用 REST API 方式**: `aliyun devops POST /organization/.../workitems/updateWorkitemField`，不能用 `aliyun devops UpdateWorkitemField`
2. **数组格式**: `updateWorkitemPropertyRequest` 必须是数组 `[{...}]`，不是对象
3. **字段名称**: 用 `fieldIdentifier`/`fieldValue`，不是 `propertyKey`/`propertyValue`

### 添加任务评论

```bash
aliyun devops POST /organization/<org-id>/workitems/comment \
  --body '{
    "workitemIdentifier": "<workitem-id>",
    "content": "评论内容，支持 Markdown",
    "formatType": "MARKDOWN"
  }'
```

**body 参数:**

| 参数 | 说明 |
|------|------|
| `workitemIdentifier` | 工作项 ID |
| `content` | 评论内容 |
| `formatType` | **必填**，可选值：`MARKDOWN` 或 `RICHTEXT` |

**返回示例:**

```json
{
  "success": true,
  "Comment": {
    "Id": 19235820,
    "content": "评论内容",
    "formatType": "MARKDOWN",
    "createTime": 1768216995000
  }
}
```

### 编辑评论

**⚠️ 无 MCP 工具，只能用 CLI。** 需要先通过 `mcp__yunxiao__list_work_item_comments` 获取 commentId。

```bash
aliyun devops UpdateWorkitemComment \
  --organizationId <org-id> \
  --body '{
    "workitemIdentifier": "<workitem-id>",
    "commentId": <comment-id>,
    "content": "更新后的评论内容",
    "formatType": "MARKDOWN"
  }'
```

**body 参数:**

| 参数 | 说明 |
|------|------|
| `workitemIdentifier` | 工作项 ID（hash ID，不是 serialNumber） |
| `commentId` | 评论 ID（数字，从 `list_work_item_comments` 获取） |
| `content` | 新的评论内容 |
| `formatType` | `MARKDOWN` 或 `RICHTEXT` |

> 注意：MCP `create_work_item_comment` 创建的评论默认为 RICHTEXT 格式。如需纯文本效果，用此 API 编辑为 `formatType: "MARKDOWN"`。

### 查询工作流（MCP）

更新状态前，查询当前工作项类型允许的状态流转路径：

```python
mcp__yunxiao__get_work_item_workflow(
    organizationId="<org-id>",
    projectId="<project-id>",
    workItemTypeId="<workitem-type-id>"
)
# 返回 statuses 列表，包含所有可用状态及其 id
```

> ⚠️ Bug 和 Task 的工作流不同，且不同项目可能自定义了不同工作流。不要硬编码状态 ID，先查询再流转。

### 完整示例：完成任务并添加评论

```bash
ORG_ID="<your-org-id>"
WORKITEM_ID="<your-workitem-id>"

# 1. 更新状态为已完成
aliyun devops POST /organization/${ORG_ID}/workitems/updateWorkitemField \
  --body "{
    \"workitemIdentifier\": \"${WORKITEM_ID}\",
    \"updateWorkitemPropertyRequest\": [
      {\"fieldIdentifier\": \"status\", \"fieldValue\": \"100014\"}
    ]
  }"

# 2. 添加完成评论
aliyun devops POST /organization/${ORG_ID}/workitems/comment \
  --body "{
    \"workitemIdentifier\": \"${WORKITEM_ID}\",
    \"content\": \"## 实现完成\\n\\n- 功能已实现\\n- 测试已通过\",
    \"formatType\": \"MARKDOWN\"
  }"
```

## 发布管理

### 创建 Tag

```bash
aliyun devops CreateTag \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --tagName v1.0.0 \
  --ref main \
  --message "Release v1.0.0"
```

## 故障排查

完整的错误信息和修复方案，见 [cheatsheet.md](cheatsheet.md) 的「错误信息 → 修复方案」章节。

## 参考链接

- [Codeup OpenAPI](https://help.aliyun.com/zh/yunxiao/developer-reference/codeup-openapi-collection/)
- [阿里云 CLI 文档](https://help.aliyun.com/document_detail/121541.html)
- [RAM 控制台](https://ram.console.aliyun.com/)
