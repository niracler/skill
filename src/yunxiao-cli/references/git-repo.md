# git-repo 安装与命令

阿里巴巴的 git-repo 是 AGit-Flow 工作流的命令行工具。**不是 Google 的 repo 工具。**

## 安装

### 第 1 步：下载

从 [GitHub Releases](https://github.com/alibaba/git-repo-go/releases) 下载：

```bash
# macOS arm64 (Apple Silicon)
curl -L -o /tmp/git-repo.tar.gz \
  "https://github.com/alibaba/git-repo-go/releases/download/v0.7.8/git-repo-0.7.8-macOS-arm64.tar.gz"

# macOS amd64 (Intel)
curl -L -o /tmp/git-repo.tar.gz \
  "https://github.com/alibaba/git-repo-go/releases/download/v0.7.8/git-repo-0.7.8-macOS-amd64.tar.gz"

# Linux amd64
curl -L -o /tmp/git-repo.tar.gz \
  "https://github.com/alibaba/git-repo-go/releases/download/v0.7.8/git-repo-0.7.8-linux-amd64.tar.gz"
```

### 第 2 步：安装

```bash
cd /tmp && tar -xzf git-repo.tar.gz
mkdir -p ~/.local/bin
cp git-repo-*/git-repo ~/.local/bin/
chmod +x ~/.local/bin/git-repo
```

添加到 PATH（在 `~/.zshrc` 或 `~/.bashrc` 中添加）：
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 第 3 步：配置 git 别名

原始命令是 `git-repo upload --single`。配置别名方便使用：

```bash
# 创建包装脚本
cat > ~/.local/bin/git-pr << 'SCRIPT'
#!/bin/bash
~/.local/bin/git-repo upload --single "$@"
SCRIPT
chmod +x ~/.local/bin/git-pr

# 设置 git 别名
git config --global alias.pr '!git-pr'
git config --global alias.peer-review '!git-pr'
```

### 第 4 步：验证

```bash
git-repo --version          # 应显示: git-repo version 0.7.8
git pr --help               # 应显示 upload 命令帮助
```

## 核心命令

### 创建 MR（提交未推送）

最简单的场景：本地有新提交，还没推送到远程。

```bash
# 打开编辑器填写标题/描述
git pr

# 或指定评审人
git pr --reviewers alice@example.com,bob@example.com
```

### 创建 MR（提交已推送） ⚠️ 重要

当提交已经推送到远程 feature 分支时，简单的 `git pr` 会报错：

```
NOTE: no branches ready for upload
```

**解决方案**：使用 `--cbr --dest` 明确指定分支：

```bash
# 交互式（打开编辑器）
git-repo upload --single --cbr --dest main

# 非交互式（脚本使用）
yes | git-repo upload --single --cbr --dest main \
  --title "feat: your title" \
  --description "Description here" \
  --no-edit
```

**参数说明**：
| 参数 | 作用 |
|------|------|
| `--single` | 单仓库模式（非 monorepo） |
| `--cbr` | 使用当前分支（Current Branch） |
| `--dest main` | MR 目标分支（**必须指定**） |
| `--title` | MR 标题 |
| `--description` | MR 描述 |
| `--no-edit` | 跳过编辑器 |
| `--draft` | 草稿模式 |
| `--dryrun` | 预览模式，不实际创建 |

**关于 `yes |`**：`--no-edit` 只跳过编辑器，不跳过 (y/N) 确认提示。脚本中必须用 `yes |` 自动确认。

### 更新已有 MR

```bash
# 方式 1：直接推送新提交（MR 自动更新）
git push origin <branch>

# 方式 2：使用 git-repo
git-repo upload --single --change <MR-ID>
```

### 下载 MR 代码评审

```bash
git-repo download <MR-ID>
```

## 编辑器字段

交互式创建时，编辑器会显示以下字段：

```
# [Title]       : MR 标题（一行）

# [Description] : 详细描述（多行）

# [Issue]       : 关联的 Issue ID（多行）

# [Reviewer]    : 评审人邮箱（每行一个）

# [Cc]          : 抄送人邮箱（每行一个）

# [Draft]       : yes/no 草稿模式

# [Private]     : yes/no 私有模式
```

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| "no branches ready for upload" | 提交已推送到远程 | 使用 `--cbr --dest main` |
| "remote is not reviewable" | 仓库不是 Codeup | git-repo 只支持 Codeup |
| "no upstream" 错误 | 分支未跟踪远程 | `git branch -u origin/<branch>` |
| "no new commits" | 本地没有新提交 | 先提交更改 |
| 脚本卡在 (y/N) | `--no-edit` 不跳过确认 | 使用 `yes \|` 管道 |
| 命令找不到 | PATH 未配置 | 检查 `~/.local/bin` 在 PATH 中 |
| 未提交的更改警告 | 工作区有改动 | 先 commit 或 stash |

## 参考链接

- [GitHub Releases](https://github.com/alibaba/git-repo-go/releases)
- [官方文档](https://help.aliyun.com/zh/yunxiao/user-guide/installation-and-configuration)
- [AGit-Flow 工作流介绍](https://help.aliyun.com/document_detail/153798.html)
