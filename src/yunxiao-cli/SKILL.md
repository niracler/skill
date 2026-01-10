---
name: yunxiao-cli
description: Use when working with Alibaba Cloud DevOps (Yunxiao/云效), including Codeup code review (MR/PR), git-repo commands (git pr, git peer-review), push review mode, release tags, or Projex tasks.
---

# 云效 CLI

阿里云云效 DevOps 命令行工具。涵盖代码评审、发布管理和任务跟踪。

## 依赖工具

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| Git | 所有操作 | 大多数系统已预装 |
| git-repo | `git pr` 命令 | 见 [git-repo.md](references/git-repo.md) |
| aliyun CLI | OpenAPI 调用 | `brew install aliyun-cli` 或 [下载](https://github.com/aliyun/aliyun-cli/releases) |

**无需安装:** Push Review Mode (`git push -o review=...`) 使用标准 Git 即可。

## 工具选择

| 任务 | 首选方案 | 备选方案 |
|------|----------|----------|
| 创建 MR | `git pr` (git-repo) | `git push -o review=new` |
| 更新 MR | `git pr` | `git push -o review=<id>` |
| 创建 Tag | `git tag` + `git push` | OpenAPI CreateTag |
| 查看任务 | Projex 网页端 | OpenAPI |

**注意:** git-repo 不是 Google 的 repo 工具，而是阿里巴巴为 AGit-Flow 工作流开发的工具。

## 快速参考

### 创建合并请求

**方案 A: git-repo (需要安装 + 配置别名)**
```bash
# 基本用法 - 打开编辑器填写标题/描述
git pr

# 指定评审人
git pr --reviewers user1@example.com,user2@example.com

# 草稿模式
git pr --draft

# 更新已有 MR
git pr --change <MR-ID>
```

**方案 B: Push Review Mode (零安装)**
```bash
# 创建新 MR
git push -o review=new

# 更新指定 MR
git push -o review=<MR-ID>

# 跳过评审 (需要推送权限)
git push -o review=no
```

### 创建发布 Tag

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## 常见错误

| 错误 | 解决方案 |
|------|----------|
| 混淆 Google repo | 阿里巴巴的 git-repo 是不同的工具，从 [GitHub](https://github.com/alibaba/git-repo-go/releases) 下载 |
| `git pr` 命令找不到 | 安装后需要配置 git 别名，见 [git-repo.md](references/git-repo.md) |
| 分支未跟踪远程 | 先运行 `git branch -u origin/<branch>` |
| 没有新提交 | 先提交更改再运行 `git pr` |
| OpenAPI "用户未关联云效" | RAM 用户需要添加到云效组织成员 |

## 详细指南

- **git-repo 安装与命令:** 见 [references/git-repo.md](references/git-repo.md)
- **Push Review Mode 选项:** 见 [references/push-review.md](references/push-review.md)
- **OpenAPI 参考:** 见 [references/openapi.md](references/openapi.md)
