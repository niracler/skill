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
aliyun devops ListOrganizations
```

### 列出仓库

```bash
aliyun devops ListRepositories --organizationId <org-id>
```

### 列出项目

```bash
aliyun devops ListProjects --organizationId <org-id> --category Project
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

### 列出合并请求

```bash
aliyun devops ListMergeRequests \
  --organizationId <org-id> \
  --repositoryId <repo-id> \
  --state opened
```

## 获取 ID

| ID | 如何获取 |
|----|----------|
| organizationId | `aliyun devops ListOrganizations` |
| repositoryId | `aliyun devops ListRepositories --organizationId <org-id>` |

## 故障排查

| 错误 | 解决方案 |
|------|----------|
| "用户失败，请确认已关联至云效账号" | RAM 用户需要添加到云效组织成员 |
| "category is mandatory" | 添加 `--category Project` 参数 |
| "spaceType is mandatory" | 查看 API 文档确认必需参数 |

## 参考链接

- [Codeup OpenAPI](https://help.aliyun.com/zh/yunxiao/developer-reference/codeup-openapi-collection/)
- [阿里云 CLI 文档](https://help.aliyun.com/document_detail/121541.html)
- [RAM 控制台](https://ram.console.aliyun.com/)
