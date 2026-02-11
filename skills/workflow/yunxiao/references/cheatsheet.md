# 云效 CLI Cheatsheet（AI 助手专用）

**本文档专为 AI 助手设计，包含所有必须遵守的规则，避免踩坑。**

## 黄金法则

### 1. 获取组织 ID 必须加 `--minAccessLevel 5`

```bash
# ✅ 正确
aliyun devops ListOrganizations --minAccessLevel 5

# ❌ 错误 - 可能返回空或错误的组织
aliyun devops ListOrganizations
```

### 2. 更新任务状态必须用 REST API 方式

```bash
# ✅ 正确 - REST API 方式
aliyun devops POST /organization/<org-id>/workitems/updateWorkitemField --body '...'

# ❌ 错误 - 命令行参数方式不工作
aliyun devops UpdateWorkitemField --organizationId <org-id> --body '...'
```

### 3. `updateWorkitemPropertyRequest` 必须是数组

```bash
# ✅ 正确 - 数组格式
"updateWorkitemPropertyRequest": [{"fieldIdentifier": "status", "fieldValue": "100014"}]

# ❌ 错误 - 对象格式
"updateWorkitemPropertyRequest": {"fieldIdentifier": "status", "fieldValue": "100014"}
```

### 4. 字段名是 `fieldIdentifier`/`fieldValue`

```bash
# ✅ 正确
{"fieldIdentifier": "status", "fieldValue": "100014"}

# ❌ 错误 - 这些名字看起来对但实际不工作
{"propertyKey": "status", "propertyValue": "100014"}
```

### 5. 评论必须指定 `formatType`

```bash
# ✅ 正确
{"content": "...", "formatType": "MARKDOWN"}

# ❌ 错误 - 缺少 formatType
{"content": "..."}
```

### 6. 获取状态列表必须加 `--workitemCategoryIdentifier`

```bash
# ✅ 正确
aliyun devops ListWorkItemWorkFlowStatus \
  --workitemCategoryIdentifier Task \
  ...

# ❌ 错误 - 缺少必需参数
aliyun devops ListWorkItemWorkFlowStatus \
  --workitemTypeIdentifier <id> \
  ...
```

### 7. 列出项目必须加 `--category Project`

```bash
# ✅ 正确
aliyun devops ListProjects --organizationId <id> --category Project

# ❌ 错误
aliyun devops ListProjects --organizationId <id>
```

### 8. 创建任务时重复字段必须同时提供

```bash
# ✅ 正确 - 同时提供两个字段，值相同
{
  "space": "xxx",
  "spaceIdentifier": "xxx",
  "workitemType": "yyy",
  "workitemTypeIdentifier": "yyy"
}

# ❌ 错误 - 只提供其中一个
{
  "spaceIdentifier": "xxx",
  "workitemTypeIdentifier": "yyy"
}
```

### 9. 创建 MR 必须提供三个额外字段

```bash
# ✅ 正确
{
  "sourceBranch": "...",
  "targetBranch": "main",
  "sourceProjectId": <repo-id>,    # 必须
  "targetProjectId": <repo-id>,    # 必须
  "createFrom": "WEB"              # 必须
}

# ❌ 错误 - 缺少这三个字段
{
  "sourceBranch": "...",
  "targetBranch": "main"
}
```

### 10. 仓库 ID 字段是 `Id`（大写 I）

```bash
# ✅ 正确 - 使用大写 Id
aliyun devops ListRepositories --organizationId <org-id> \
  | jq '.result[] | {Id, name}'

# ❌ 错误 - 小写 id 会返回 null
aliyun devops ListRepositories --organizationId <org-id> \
  | jq '.result[] | {id, name}'
```

### 11. 创建任务前必须查询必填字段

```bash
# ✅ 正确 - 先查询字段配置，再创建任务
# 使用 MCP 工具：
mcp__yunxiao__get_work_item_type_field_config(
  organizationId="...", projectId="...", workItemTypeId="..."
)

# ❌ 错误 - 直接创建任务，遇到「字段【xxx】不能为空」错误
aliyun devops CreateWorkitem --body '{...}'  # 缺少必填自定义字段
```

### 12. `assignedTo` 是必填的，需要用户 accountId

```bash
# 获取用户 accountId
aliyun devops ListOrganizationMembers --organizationId <org-id> \
  | jq -r '.members[] | "\(.accountId): \(.organizationMemberName)"'

# ⚠️ 没有「获取当前用户」的 API，必须从成员列表中查找
```

### 13. 从 git remote 提取组织 ID

```bash
# Codeup 仓库的 remote 格式：
# git@codeup.aliyun.com:<org-id>/<namespace>/<repo>.git

# 提取组织 ID
git remote get-url origin | sed -E 's|.*codeup.aliyun.com[:/]([^/]+)/.*|\1|'
```

### 14. `get_work_item` 支持 serialNumber

```bash
# ✅ 正确 - 直接用 serialNumber
mcp__yunxiao__get_work_item(workItemId="MYCP-106")

# ✅ 也正确 - 用完整 hash ID
mcp__yunxiao__get_work_item(workItemId="ecfa20663d570c7438420a3c98")

# 不需要先查询完整 ID，serialNumber（如 MYCP-106）可直接使用
```

### 15. Bug 状态流转受工作流限制

```bash
# ✅ 正确 - 先查询工作流，再按允许的路径流转
mcp__yunxiao__get_work_item_workflow(
  organizationId="...", projectId="...", workItemTypeId="..."
)

# ❌ 错误 - 直接跳到目标状态，可能报"当前状态:X不能流转到目标状态:Y"
# Bug 的"待确认"可以直接到"已修复"，但不能到"开发完成"
```

### 16. 获取仓库 ID 优先用 MCP 工具

```bash
# ✅ 推荐 - MCP 工具更可靠
mcp__yunxiao__list_repositories(organizationId="...", search="repo-name")

# ⚠️ CLI 可能报 SYSTEM_UNAUTHORIZED_ERROR
aliyun devops ListRepositories --organizationId <org-id>
```

## 常用状态 ID

### Task（通用）

| 状态 | identifier |
|------|------------|
| 待处理 | `100005` |
| 处理中 | `100010` |
| 已完成 | `100014` |

### Bug（因项目而异，建议用 `get_work_item_workflow` 查询）

| 状态 | identifier |
|------|------------|
| 待确认 | `28` |
| 已修复 | `29` |
| 再次打开 | `30` |
| 暂不修复 | `31` |
| 已关闭 | `100085` |

## 错误信息 → 修复方案

| 看到这个错误 | 立即这样修复 |
|-------------|-------------|
| `组织不存在` | 加 `--minAccessLevel 5` 重新获取组织 ID |
| 仓库 ID 返回 `null` | jq 改用大写 `.Id`（不是 `.id`） |
| `用户失败，请确认已关联至云效账号` | RAM 用户需要添加到云效组织成员 |
| `category is mandatory` | 加 `--category Project` |
| `spaceType is mandatory` | 加 `--spaceType Project` |
| `Missingspace` / `MissingspaceIdentifier` | body 中同时加 `space` 和 `spaceIdentifier` |
| `MissingworkitemType` | body 中同时加 `workitemType` 和 `workitemTypeIdentifier` |
| `MissingworkitemCategoryIdentifier` | 加 `--workitemCategoryIdentifier Task` |
| `MissingfieldIdentifier` | 用 `fieldIdentifier` 不是 `propertyKey` |
| `InvalidJSON Array parsing error` | `updateWorkitemPropertyRequest` 改成数组 `[{...}]` |
| `MissingformatType` | 加 `"formatType": "MARKDOWN"` |
| `MissingsourceProjectId` | 加 `sourceProjectId` 和 `targetProjectId` |
| `MissingcreateFrom` | 加 `"createFrom": "WEB"` |
| `MissingassignedTo` | 加 `assignedTo`（用户 accountId，从成员列表获取） |
| `字段【xxx】不能为空` | 先用 MCP 查询必填字段配置，再添加到 `fieldValueList` |
| ListMergeRequests 的 `--repositoryId` 无效 | 该 API 不支持按仓库过滤，使用 `--groupIds` |
| UpdateWorkitemField 参数不识别 | 用 REST API：`aliyun devops POST /organization/.../workitems/updateWorkitemField` |
| `当前状态:X不能流转到目标状态:Y` | 先用 `get_work_item_workflow` 查询允许的状态流转路径 |
| `SYSTEM_UNAUTHORIZED_ERROR` (ListRepositories) | 改用 MCP 工具 `mcp__yunxiao__list_repositories` |
