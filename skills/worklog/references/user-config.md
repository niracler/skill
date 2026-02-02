# 用户配置

worklog skill 的身份和数据源配置。

## 用户身份

```yaml
# 云效用户名（用于识别"我的"任务和 Bug）
yunxiao_username: "<your-yunxiao-username>"

# 云效组织 ID
yunxiao_org_id: "<your-yunxiao-org-id>"

# GitHub 用户名（用于查询 events 和 PR）
github_username: "<your-github-username>"
```

## 默认行为

如果没有配置：

- **本地 git 统计** — 使用 `git config user.name` 作为 author 过滤（stats.sh 默认行为）
- **云效数据** — 需要 yunxiao_username 和 yunxiao_org_id，否则跳过并标注"未配置"
- **GitHub 数据** — 需要 github_username，否则跳过并标注"未配置"

## 如何使用

1. 将上述配置根据个人情况修改
2. worklog skill 在执行时会读取此文件获取身份信息
3. 如果字段为空或为占位符，对应的远程数据源将被跳过
