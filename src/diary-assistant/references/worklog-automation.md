# Work Log 自动化

从版本控制和项目管理工具自动获取今日工作记录，减少手动输入。

## 数据源

### 1. GitHub

```bash
# 获取用户名
USERNAME=$(gh api user --jq '.login')

# 查看今日 push 事件
gh api "/users/${USERNAME}/events" --jq '
  .[] | select(.type == "PushEvent") |
  {repo: .repo.name, time: .created_at, commits: [.payload.commits[].message]}'
```

### 2. 本地 Git 仓库

```bash
# 查看今日提交（指定仓库目录）
git -C /path/to/repo log --oneline --since="00:00:00" --until="23:59:59" --all

# 遍历多个仓库
for repo in ~/code/project/repos/*/; do
  name=$(basename "$repo")
  commits=$(cd "$repo" && git log --oneline --since="today" --all 2>/dev/null | head -5)
  if [ -n "$commits" ]; then
    echo "=== $name ==="
    echo "$commits"
  fi
done
```

### 3. 云效（Alibaba DevOps）

调用 `yunxiao-cli` skill 获取：

```bash
# 列出组织
aliyun devops ListOrganizations --minAccessLevel 5 | jq -r '.result[] | "\(.organizationId): \(.organizationName)"'

# 列出项目任务
aliyun devops ListWorkitems \
  --organizationId <org-id> \
  --spaceIdentifier <project-id> \
  --spaceType Project \
  --category Task \
  | jq -r '.workitems[:10] | .[] | "\(.identifier): \(.subject) [\(.status)]"'
```

## 使用流程

1. **询问用户** - 「要我从 git/云效自动获取今天的工作记录吗？」
2. **识别数据源** - 根据当前目录或用户配置，判断使用哪些数据源
3. **汇总展示** - 将获取到的提交/任务整理成 Work Log 格式
4. **用户确认** - 让用户补充或修正

## 输出格式示例

```markdown
### 云效 - AzoulaLite Backend

- **发布 v0.5.0 / API 1.4.0**
- feat: OpenAPI 一致性修复
- fix: python-multipart 安全漏洞

### GitHub

- **niracler/skill**: 新增 schedule-manager Skill
- **niracler/ha-core**: sunricher-dali-energy-sensor 分支更新
```

## 注意事项

- 自动获取的是「做了什么」，但用户可能需要补充「为什么做」和「遇到的挑战」
- 不要完全依赖自动化，仍需启发用户思考和补充
