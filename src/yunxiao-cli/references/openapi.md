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

### 创建 Tag

```bash
aliyun devops CreateTag \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --tagName v1.0.0 \
  --ref main \
  --message "Release v1.0.0"
```

### 列出合并请求

```bash
# 查询所有 MR
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --pageSize 50

# 按时间范围查询（createdBefore 是起始时间，createdAfter 是截止时间）
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --createdBefore "2026-01-06T00:00:00Z" \
  --orderBy created_at \
  --pageSize 50
```

**常用参数:**

- `--createdBefore`: 起始创建时间 (ISO 8601 格式)
- `--createdAfter`: 截止创建时间
- `--authorIds`: 按创建人过滤（阿里云账号 ID，逗号分隔）
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
| "category is mandatory" | 添加 `--category Project` 参数 |
| "spaceType is mandatory" | 查看 API 文档确认必需参数 |
| ListMergeRequests 的 `--repositoryId` 无效 | 该 API 不支持按仓库过滤，使用 `--groupIds` 过滤代码组 |

## 参考链接

- [Codeup OpenAPI](https://help.aliyun.com/zh/yunxiao/developer-reference/codeup-openapi-collection/)
- [阿里云 CLI 文档](https://help.aliyun.com/document_detail/121541.html)
- [RAM 控制台](https://ram.console.aliyun.com/)
