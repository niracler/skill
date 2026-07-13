# 周报数据源

只在执行数据采集时读取本文件。开始采集前，检查所有必需工具、认证和权限。工具缺失、
凭据无效、配置错误或权限不足时停止并修复。网络超时、限流或远程服务异常属于临时故障，
无论在预检还是采集阶段发现，都继续使用其余来源并记录数据缺口。

## Obsidian 工作日志

优先从 Obsidian 的 macOS 配置中定位已打开的 vault；存在多个 vault 时请求选择。读取报告
周期内每个工作日日记的 `## 2 Work Log`。日记缺失或章节不存在时停止并请求路径，不创建
新日记或章节。

## 飞书项目

飞书项目指 `project.feishu.cn`，使用官方 `meegle` CLI，不使用 `lark-task` 或通用
`lark-cli` 代替。已安装 `meegle` Agent Skill 时先读取；否则通过 `meegle inspect` 获取
当前命令参数，不猜测项目键和字段。

```bash
meegle auth status
meegle mywork todo --action done --page-num 1 --auto-paginate
meegle mywork todo --action this_week --page-num 1 --auto-paginate
meegle mywork todo --action overdue --page-num 1 --auto-paginate
```

- 「已办」按完成时间或更新时间筛选到报告周期，用于补充本周成果。
- 「本周待办」用于核对未完成事项。
- 「逾期」用于识别阻塞和顺延事项。
- 标题、状态或项目归属不足时，再读取工作项详情。

## GitLab MCP

先查看当前会话已注册的 MCP 工具，找到同时提供连接检查、用户查询、项目搜索、MR 和 Issue
读取能力的 GitLab MCP。工具命名空间由本地配置决定，不硬编码 `mcp__GitLab__*` 名称；
缺少所需能力时提示在 Codex MCP 配置中启用或更新已安装的 GitLab MCP，设置自建地址和
访问令牌，然后重启会话。

调用实际工具清单中的连接检查能力。从 `~/code/*/` 的本地仓库远端提取候选项目路径，排除
`github.com`，再按已发现工具的参数结构执行等价的只读项目搜索。若工具支持以下字段，使用：

```json
{
  "project_id": "group/project",
  "scope": "merge_requests",
  "search": "",
  "page": 1,
  "per_page": 1,
  "order_by": "created_at",
  "sort": "desc"
}
```

空搜索词不被当前 MCP 接受时，将 GitLab 标记为采集失败，不改用关键词代替完整枚举。

使用 `users` 范围，结合 `git config user.name` 和 `git config user.email` 解析当前用户；
匹配不唯一时请求确认。对每个项目分别读取 `merge_requests` 和 `issues`，`per_page` 设为
`100`，从第 1 页递增到返回数量少于 `100`。

- MR 保留本人在报告周期内创建的打开、合并或关闭记录。
- Issue 保留本人创建或负责，且创建时间或更新时间位于报告周期内的记录。
- 标题和描述不足时，再读取 MR、Issue 或 MR 提交详情。

## GitHub

查询本人创建或在报告周期内更新的 PR，以及本人创建或负责的 Issue。`{end_date}` 为当前
周最后一个工作日：大周使用周六，小周使用周五。

```bash
gh search prs --author=@me --created="{monday}..{end_date}" \
  --limit 100 --json repository,title,number,state,url,createdAt,updatedAt
gh search prs --author=@me --updated="{monday}..{end_date}" \
  --limit 100 --json repository,title,number,state,url,createdAt,updatedAt
gh search issues --author=@me --created="{monday}..{end_date}" \
  --limit 100 --json repository,title,number,state,url,createdAt,updatedAt,assignees
gh search issues --assignee=@me --updated="{monday}..{end_date}" \
  --limit 100 --json repository,title,number,state,url,createdAt,updatedAt,assignees
```

合并重复结果。只有与历史周报、Obsidian、飞书项目、GitLab 或本周本地 Git 活动明确对应
的仓库才直接归入公司周报；其余结果使用匿名名称列为候选并请求确认。任一查询恰好返回
100 条时停止并缩小仓库范围。标题不足时使用 `gh pr view` 或 `gh issue view` 补充详情。

## 本地 Git

只扫描 `~/code/*/`，不递归扫描旧的嵌套仓库目录。对每个仓库执行：

```bash
git log --oneline --since="{start_time}" --until="{end_time}" \
  --author="{user}" --all
```

`{user}` 取自 `git config user.name`；`{start_time}` 和 `{end_time}` 使用大小周章节定义的
本地时区半开区间。按项目和仓库分组，用于发现遗漏并核对远程活动。

## 降级与错误处理

- 工具原始响应只保留在当前执行上下文，不写入仓库或长期临时文件。
- 错误信息对外展示时隐藏项目、仓库、主机和人员标识。
- Obsidian 目标日记或写入位置无法定位时停止，因为无法完成审阅与写回。
- 飞书项目、GitLab 或 GitHub 发生网络超时、限流或远程服务异常时，继续使用其余来源生成
  草稿；该规则不取决于故障发生在预检还是采集阶段。
- 本地 Git 的个别仓库读取失败时跳过该仓库；Git 本身不可用属于预检失败。
- 在正式周报之外列出缺失来源、影响范围和重试方式，不把采集故障写入周报正文。
