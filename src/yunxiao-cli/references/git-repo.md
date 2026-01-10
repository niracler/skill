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

### git pr / git-repo upload

从命令行创建或更新合并请求。

```bash
# 基本用法 - 打开编辑器填写标题/描述
git pr

# 指定评审人
git-repo upload --single --reviewers alice@example.com,bob@example.com

# 创建草稿
git-repo upload --single --draft

# 更新已有 MR
git-repo upload --single --change 888

# 预览模式（不实际上传）
git pr --dryrun
```

**编辑器字段:**
- `[Title]`: MR 标题
- `[Description]`: 详细描述
- `[Reviewer]`: 每行一个邮箱
- `[Draft]`: yes/no 草稿模式

### git-repo download

下载 MR 代码到本地评审。

```bash
git-repo download <MR-ID>
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| "remote is not reviewable" | 只能用于 Codeup 仓库，不支持 GitHub |
| "no upstream" 错误 | 运行 `git branch -u origin/<branch>` |
| "no new commits" | 先提交更改 |
| 命令找不到 | 检查 PATH 是否包含 `~/.local/bin` |
| 未提交的更改警告 | 先提交或 stash 更改 |

## 参考链接

- [GitHub Releases](https://github.com/alibaba/git-repo-go/releases)
- [官方文档](https://help.aliyun.com/zh/yunxiao/user-guide/installation-and-configuration)
