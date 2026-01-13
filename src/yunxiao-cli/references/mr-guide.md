# MR 操作完整指南

通过阿里云 CLI 管理云效代码评审（合并请求）。

## 前置准备

### 安装配置 aliyun CLI

如果尚未配置，参考 [openapi.md](openapi.md) 的"配置"章节完成：
1. 安装 aliyun CLI
2. 创建 AccessKey
3. 运行 `aliyun configure`

### 获取必需 ID

```bash
# 获取组织 ID（必须加 --minAccessLevel 5）
aliyun devops ListOrganizations --minAccessLevel 5 \
  | jq -r '.result[] | "\(.organizationId): \(.organizationName)"'

# 获取仓库 ID
aliyun devops ListRepositories --organizationId <org-id> \
  | jq '.result[] | {Id, name}'
```

---

## 常用操作

### 创建 MR

**完整命令：**

```bash
# 1. 确保分支已推送到远程
git push -u origin <your-branch>

# 2. 创建 MR
aliyun devops CreateMergeRequest \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --body '{
    "title": "feat: your title",
    "description": "## Summary\n\nDescription here",
    "sourceBranch": "<your-branch>",
    "targetBranch": "main",
    "sourceProjectId": <repo-id>,
    "targetProjectId": <repo-id>,
    "createFrom": "WEB"
  }'
```

**必填参数说明：**

| 参数 | 说明 |
|------|------|
| `title` | MR 标题，建议遵循 conventional commits 格式 |
| `sourceBranch` | 源分支名（你的开发分支） |
| `targetBranch` | 目标分支名（通常是 `main`） |
| `sourceProjectId` | 源仓库 ID（值同 repositoryId） |
| `targetProjectId` | 目标仓库 ID（值同 repositoryId） |
| `createFrom` | 必须为 `"WEB"` |

**显示效果：** 创建的 MR 会显示分支名（如 "将 feature-branch 合并至 main"）。

### 更新已有 MR

MR 创建后，只需推送新提交，MR 会自动更新：

```bash
git add .
git commit -m "fix: address review comments"
git push origin <your-branch>
```

### 查看 MR 列表

```bash
# 列出最近的 MR
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --orderBy created_at \
  --pageSize 20

# 按时间范围查询
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --createdAfter "2026-01-01T00:00:00Z" \
  --orderBy created_at \
  --pageSize 50
```

**常用过滤参数：**

| 参数 | 说明 |
|------|------|
| `--createdBefore` | 截止创建时间 (ISO 8601) |
| `--createdAfter` | 起始创建时间 |
| `--authorIds` | 按创建人过滤 |
| `--orderBy` | 排序字段 (`created_at` 或 `updated_at`) |
| `--page` / `--pageSize` | 分页参数 |

### 获取 MR 详情

```bash
aliyun devops GetMergeRequest \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --localId <mr-local-id>
```

---

## 可选功能

### 指定评审人

在 body 中添加 `reviewerIds` 数组：

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

### 关联工作项

在 body 中添加 `workItemIds` 数组：

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

---

## 故障排查

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `MissingsourceProjectId` | 缺少必填参数 | 添加 `sourceProjectId` 和 `targetProjectId` |
| `MissingcreateFrom` | 缺少必填参数 | 添加 `"createFrom": "WEB"` |
| `组织不存在` | organizationId 错误 | 用 `ListOrganizations --minAccessLevel 5` 获取 |
| `Repository not found` | repositoryId 错误 | 用 `ListRepositories` 获取正确 ID |
| `Branch not found` | 分支未推送到远程 | 先执行 `git push -u origin <branch>` |
| `用户失败，请确认已关联至云效账号` | RAM 用户未添加到云效 | 在云效控制台添加 RAM 用户为组织成员 |

---

## 参考链接

- [Codeup OpenAPI 文档](https://help.aliyun.com/zh/yunxiao/developer-reference/codeup-openapi-collection/)
- [完整 API 参考](openapi.md)
