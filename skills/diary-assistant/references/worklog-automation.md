# Work Log 自动化

从云效和 GitHub 自动获取今日工作记录，两个数据源相互独立，可并行获取以提高效率。

## 并行获取策略

**以下两个数据源相互独立，可并行获取：**

```text
┌─ 数据源 1: 云效数据（yunxiao skill）（独立，不依赖 GitHub 数据）
│   - MR: 今天创建/合并的 Merge Request
│   - Bug: 今天新增/关闭的，标注哪些是我的
│   - 任务: 今天更新的任务
│
└─ 数据源 2: GitHub 数据（gh api）（独立，不依赖云效数据）
    - 今日所有仓库的提交
    - PR 活动（如有）
    ↓
全部完成后，整理成 Work Log
```

## 数据源

### 1. 云效（通过 yunxiao skill）

独立获取云效数据（不依赖 GitHub 数据的结果）：

如果 yunxiao skill 可用，按其指令获取今天的 MR、Bug、任务记录；
否则使用 aliyun CLI 手动查询（见 yunxiao skill 的 references/openapi.md）。

配置参数：

- 组织 ID: 见 [user-config.md](user-config.md)
- 用户: 见 [user-config.md](user-config.md)

### 2. GitHub（通过 gh api）

独立获取 GitHub 数据：

```bash
# 获取今日所有活动
gh api "/users/niracler/events?per_page=50" --jq '
  [.[] | select(.created_at | startswith("YYYY-MM-DD"))]
'

# 获取特定仓库的今日提交
gh api "/repos/niracler/skill/commits?since=YYYY-MM-DDT00:00:00Z" --jq '
  .[] | {sha: .sha[0:7], message: .commit.message}
'
```

### 不使用本地 Git

云效和 GitHub API 已覆盖所有工作记录，不需要从本地 git 仓库获取。

## 输出格式

使用列表形式，不用表格（参考 2026-01-27 日记格式）：

```markdown
### 云效 - Sunlite Backend

- **MR #57 合并**: chore: rename AzoulaLite to Sunlite（品牌重命名）
- **MR #56 合并**: feat(scene): implement Scene API and Node reference consistency
- **MR #58 待合并**: fix(sr-mesh): unify allocated range validation

### GitHub

- **niracler/skill**: refactor: 拆分 writing-assistant 为 3 个独立 skill
- **niracler/bokushi**: fix
- **niracler/azoulalite-dev**: 工作仓库同步

### Bug 跟踪

- 我的待处理 (4 个): MYCP-96 (修复中), MYCP-103/104/106 (待确认) → 已规划明天处理
- 今天关闭: MYCP-91, 95, 97, 98, 100 (5 个)
```

## 身份说明

根据 [user-config.md](user-config.md) 中的配置识别用户身份。

## 注意事项

- 自动获取的是「做了什么」，用户可能需要补充「为什么做」和「遇到的挑战」
- Bug 部分要区分哪些是我的，哪些是同事的
- 不要完全依赖自动化，仍需启发用户思考和补充
