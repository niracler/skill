# 云效 CLI Cheatsheet（AI 助手专用）

**本文档专为 AI 助手设计，包含所有必须遵守的规则，避免踩坑。**

---

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

---

## 常用状态 ID

| 状态 | identifier |
|------|------------|
| 待处理 | `100005` |
| 处理中 | `100010` |
| 已完成 | `100014` |

---

## 完整命令模板

### 更新任务为已完成

```bash
aliyun devops POST /organization/<ORG_ID>/workitems/updateWorkitemField \
  --body '{
    "workitemIdentifier": "<WORKITEM_ID>",
    "updateWorkitemPropertyRequest": [
      {"fieldIdentifier": "status", "fieldValue": "100014"}
    ]
  }'
```

### 添加 Markdown 评论

```bash
aliyun devops POST /organization/<ORG_ID>/workitems/comment \
  --body '{
    "workitemIdentifier": "<WORKITEM_ID>",
    "content": "评论内容",
    "formatType": "MARKDOWN"
  }'
```

### 列出任务

```bash
aliyun devops ListWorkitems \
  --organizationId <ORG_ID> \
  --spaceIdentifier <PROJECT_ID> \
  --spaceType Project \
  --category Task
```

---

## MR 操作速查

### 创建 MR（最常用）

复制后替换 `<>` 部分：

```bash
aliyun devops CreateMergeRequest \
  --organizationId <ORG_ID> \
  --repositoryId <REPO_ID> \
  --body '{
    "title": "<feat/fix/docs>: <简短描述>",
    "sourceBranch": "<你的分支名>",
    "targetBranch": "main",
    "sourceProjectId": <REPO_ID>,
    "targetProjectId": <REPO_ID>,
    "createFrom": "WEB"
  }'
```

### 查看 MR 列表

```bash
aliyun devops ListMergeRequests \
  --organizationId <ORG_ID> \
  --orderBy created_at \
  --pageSize 20
```

### 获取仓库 ID

```bash
aliyun devops ListRepositories --organizationId <ORG_ID> \
  | jq '.result[] | {Id, name}'
```

---

## 错误信息 → 修复方案

| 看到这个错误                          | 立即这样修复                                            |
| ------------------------------------- | ------------------------------------------------------- |
| `组织不存在`                          | 加 `--minAccessLevel 5` 重新获取组织 ID                 |
| `MissingworkitemCategoryIdentifier`   | 加 `--workitemCategoryIdentifier Task`                  |
| `MissingfieldIdentifier`              | 用 `fieldIdentifier` 不是 `propertyKey`                 |
| `InvalidJSON Array parsing error`     | 改成数组 `[{...}]`                                      |
| `MissingformatType`                   | 加 `"formatType": "MARKDOWN"`                           |
| `category is mandatory`               | 加 `--category Project`                                 |
| `Missingspace`                        | 同时加 `space` 和 `spaceIdentifier`                     |
| `MissingsourceProjectId`              | 加 `sourceProjectId` 和 `targetProjectId`               |
| `MissingcreateFrom`                   | 加 `"createFrom": "WEB"`                                |
| `MissingassignedTo`                   | 加 `assignedTo`（用户 accountId，从成员列表获取）       |
| `字段【xxx】不能为空`                 | 先用 MCP 查询必填字段配置，再添加到 `fieldValueList`    |