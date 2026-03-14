# Report Template

The weekly report follows this exact structure. Adapt content but preserve the hierarchy.

## Template

```markdown
### 软件研发周报（M/D - M/D）

#### 本周工作总结

{project-display-name}（{phase-name}，进度 {done}/{total}）：

- **{bold key phrase}**：{concrete description with numbers and context}
- **{bold key phrase}**：{concrete description}

{next-project-display-name}：

- **{bold key phrase}**：{concrete description}

#### 下周工作计划（M/D - M/D）

{project-display-name}（{estimated-days} 天）：

- **{bold key phrase}**：{what will be done and expected outcome}

{next-project-display-name}（{estimated-days} 天）：

- **{bold key phrase}**：{what will be done and expected outcome}

#### 其他事项

- {handoff / blocker / carry-forward note}
```

## Formatting Rules

1. **Project headers**: Use display names from schedule YAML `title` field, or reuse previous report's grouping
2. **Progress fraction**: Only for projects with schedule YAML (count done/total modules in current phase)
3. **Time estimates**: In 下周计划, include `（N 天）` when the user has expressed time allocation
4. **Bold pattern**: Start each bullet with `**bold key phrase**` followed by `：` (Chinese colon) then description
5. **Concrete details**: Always include specific numbers — commit count, test count, coverage %, API endpoint count, PR/MR numbers, issue numbers
6. **No markdown headers inside sections**: Use bold project names as line text, not `####` or `#####`

## Style Reference

The report is read by a manager who is technical but doesn't read the code.
Each bullet should answer "what was done" + "why it matters" or "what it means for the project".

Good: `**完成 auth 模块**：包含注册、登录、JWT 刷新等 9 个端点，37 个测试达到 91% 覆盖率，2 个 MR 已合并`

Bad: `完成了 auth 相关的工作` (too vague, no numbers)

Bad: `重构了 BaseService 提取 UUID 解析和成员查询逻辑到基类减少 350 行代码` (too implementation-focused, boss doesn't care about BaseService)
