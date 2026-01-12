---
name: yunxiao-cli
description: Use when working with Alibaba Cloud DevOps (Yunxiao/云效), including Codeup code review (MR/PR), git-repo commands (git pr, git peer-review), push review mode, release tags, or Projex tasks.
---

# 云效 CLI

阿里云云效 DevOps 命令行工具。涵盖代码评审、发布管理和任务跟踪。

## 已知 ID 速查表

**首次使用前必须获取这些 ID，后续可直接复用：**

```bash
# 获取组织 ID（必须加 --minAccessLevel 5）
aliyun devops ListOrganizations --minAccessLevel 5 \
  | jq -r '.result[] | "\(.organizationId): \(.organizationName)"'

# 获取项目 ID
aliyun devops ListProjects --organizationId <org-id> --category Project \
  | jq -r '.projects[] | "\(.identifier): \(.name)"'

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
```

**常见状态 ID（大多数项目通用）：**

| 状态 | identifier |
|------|------------|
| 待处理 | `100005` |
| 处理中 | `100010` |
| 已完成 | `100014` |

---

## 任务管理（一次成功模板）

### 查看任务列表

```bash
aliyun devops ListWorkitems \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --category Task \
  | jq -r '.workitems[] | "\(.identifier): \(.subject) [\(.status)]"'
```

### 更新任务状态为"已完成"

**⚠️ 必须用 REST API 方式（`aliyun devops POST /path`），不能用命令行参数方式**

```bash
aliyun devops POST /organization/<org-id>/workitems/updateWorkitemField \
  --body '{
    "workitemIdentifier": "<workitem-id>",
    "updateWorkitemPropertyRequest": [
      {"fieldIdentifier": "status", "fieldValue": "100014"}
    ]
  }'
```

**关键点：**
- `updateWorkitemPropertyRequest` 必须是**数组** `[{...}]`
- 字段名是 `fieldIdentifier` 和 `fieldValue`（不是 `propertyKey/propertyValue`）

### 添加任务评论

```bash
aliyun devops POST /organization/<org-id>/workitems/comment \
  --body '{
    "workitemIdentifier": "<workitem-id>",
    "content": "## 评论标题\n\n评论内容，支持 Markdown",
    "formatType": "MARKDOWN"
  }'
```

**关键点：** `formatType` 必须指定（`MARKDOWN` 或 `RICHTEXT`）

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

---

## MR 管理

### 创建 MR 决策流程

```
提交是否已推送到远程?
├── 否 → Push Review Mode（最简单）
│         git push -u origin <branch> -o review=new
│
└── 是 → 需要显示分支名?
          ├── 是 → aliyun CLI API（推荐）
          └── 否 → git-repo
```

### Push Review Mode（提交未推送）

```bash
git push -u origin <branch> -o review=new
```

### aliyun CLI API（提交已推送，推荐）

```bash
# 获取 Repository ID（首次需要）
aliyun devops ListRepositories --organizationId <org-id> \
  | jq '.result[] | {Id, name}'

# 创建 MR
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

**关键点：** `sourceProjectId`, `targetProjectId`, `createFrom: "WEB"` 都必须提供

### git-repo（备选，显示 commit hash）

```bash
yes | git-repo upload --single --cbr --dest main \
  --title "feat: your title" \
  --no-edit
```

### 更新已有 MR

```bash
git push origin <branch>  # MR 自动更新
```

### 查看 MR 列表

```bash
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --orderBy created_at \
  --pageSize 50
```

---

## 创建任务

```bash
aliyun devops CreateWorkitem \
  --organizationId <org-id> \
  --body '{
    "subject": "任务标题",
    "space": "<project-id>",
    "spaceIdentifier": "<project-id>",
    "spaceType": "Project",
    "category": "Task",
    "workitemType": "<task-type-id>",
    "workitemTypeIdentifier": "<task-type-id>",
    "assignedTo": "<user-id>",
    "fieldValueList": [
      {"fieldIdentifier": "<field-id>", "value": "<value>"}
    ]
  }'
```

**关键点：**
- `space` 和 `spaceIdentifier` 必须**同时提供**，值相同
- `workitemType` 和 `workitemTypeIdentifier` 必须**同时提供**，值相同

---

## 创建发布 Tag

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

---

## 常见错误速查

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `组织不存在` | organizationId 错误 | 用 `ListOrganizations --minAccessLevel 5` 获取 |
| `MissingworkitemCategoryIdentifier` | ListWorkItemWorkFlowStatus 缺参数 | 加 `--workitemCategoryIdentifier Task` |
| `MissingfieldIdentifier` | UpdateWorkitemField 参数名错误 | 用 `fieldIdentifier` 不是 `propertyKey` |
| `InvalidJSON Array parsing error` | updateWorkitemPropertyRequest 格式错误 | 必须是数组 `[{...}]` |
| `MissingformatType` | CreateWorkitemComment 缺参数 | 加 `formatType: "MARKDOWN"` |
| `category is mandatory` | ListProjects 缺参数 | 加 `--category Project` |
| `Missingspace` | CreateWorkitem 缺参数 | body 中同时包含 `space` 和 `spaceIdentifier` |
| `MissingsourceProjectId` | CreateMergeRequest 缺参数 | 加 `sourceProjectId`, `targetProjectId` |
| `MissingcreateFrom` | CreateMergeRequest 缺参数 | 加 `createFrom: "WEB"` |
| `Everything up-to-date` | Push Review 无法处理已推送的提交 | 改用 aliyun CLI 或 git-repo |
| `no branches ready for upload` | git-repo 找不到新内容 | 用 `--cbr --dest main` |
| 脚本卡在 (y/N) | git-repo 的确认提示 | 用 `yes \|` 管道 |

---

## 依赖工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| Git | 所有操作 | 大多数系统已预装 |
| aliyun CLI | OpenAPI（推荐） | `brew install aliyun-cli` |
| git-repo | `git pr` 命令 | 见 [git-repo.md](references/git-repo.md) |

---

## 详细指南

- **AI 助手必读:** 见 [references/cheatsheet.md](references/cheatsheet.md) - 所有必须遵守的规则
- **git-repo 安装与命令:** 见 [references/git-repo.md](references/git-repo.md)
- **Push Review Mode 选项:** 见 [references/push-review.md](references/push-review.md)
- **OpenAPI 参考:** 见 [references/openapi.md](references/openapi.md)