# 云效 OpenAPI 参考

通过阿里云 CLI 程序化访问云效服务。

## 配置

### 第 1 步：安装 aliyun CLI

```bash
# macOS
brew install aliyun-cli

# 或从 GitHub 下载
# https://github.com/aliyun/aliyun-cli/releases
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

## 常用操作

### 列出组织

```bash
# 只列出自己拥有的组织
aliyun devops ListOrganizations

# 列出所有组织（包括作为成员加入的）- 推荐
aliyun devops ListOrganizations --minAccessLevel 5
```

**accessLevel 说明:**

- 5: 企业外部成员
- 15: 企业成员
- 60: 企业管理员
- 70: 企业拥有者

### 列出仓库

```bash
aliyun devops ListRepositories --organizationId <org-id>
```

### 列出项目

```bash
aliyun devops ListProjects --organizationId <org-id> --category Project
```

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

### 创建 Tag

```bash
aliyun devops CreateTag \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --tagName v1.0.0 \
  --ref main \
  --message "Release v1.0.0"
```

### 创建合并请求（推荐）

当提交已推送到远程分支时，使用此 API 创建分支合并请求：

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

**与 git-repo 的区别:** 此 API 创建的 MR 会显示分支名（如 "将 feature-branch 合并至 main"），而 git-repo 创建的会显示 commit hash。

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

## 获取 ID

| ID | 如何获取 |
| --- | --- |
| organizationId | `aliyun devops ListOrganizations --minAccessLevel 5` |
| repositoryId | `aliyun devops ListRepositories --organizationId <org-id>` |
| spaceIdentifier (项目ID) | `ListProjects` 返回的 `identifier` 字段 |

## 故障排查

| 错误 | 解决方案 |
| --- | --- |
| "用户失败，请确认已关联至云效账号" | RAM 用户需要添加到云效组织成员 |
| "组织不存在" | organizationId 错误，用 `ListOrganizations --minAccessLevel 5` 获取 |
| "category is mandatory" | 添加 `--category Project` 参数 |
| "spaceType is mandatory" | 查看 API 文档确认必需参数 |
| ListMergeRequests 的 `--repositoryId` 无效 | 该 API 不支持按仓库过滤，使用 `--groupIds` 过滤代码组 |
| "Missingspace" / "MissingspaceIdentifier" | body 中同时包含 space 和 spaceIdentifier |
| "MissingworkitemType" | body 中同时包含 workitemType 和 workitemTypeIdentifier |
| "字段【xxx】不能为空" | 用 ListWorkItemAllFields 获取必填字段，在 fieldValueList 中提供 |
| "MissingworkitemCategoryIdentifier" | ListWorkItemWorkFlowStatus 加 `--workitemCategoryIdentifier Task` |
| "MissingfieldIdentifier" | UpdateWorkitemField 用 `fieldIdentifier` 不是 `propertyKey` |
| "InvalidJSON Array parsing error" | `updateWorkitemPropertyRequest` 必须是数组 `[{...}]` |
| "MissingformatType" | CreateWorkitemComment 加 `formatType: "MARKDOWN"` |
| UpdateWorkitemField 参数不识别 | 用 REST API：`aliyun devops POST /organization/.../workitems/updateWorkitemField` |

## 参考链接

- [Codeup OpenAPI](https://help.aliyun.com/zh/yunxiao/developer-reference/codeup-openapi-collection/)
- [阿里云 CLI 文档](https://help.aliyun.com/document_detail/121541.html)
- [RAM 控制台](https://ram.console.aliyun.com/)
