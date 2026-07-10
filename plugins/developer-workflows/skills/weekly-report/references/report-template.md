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
5. **Concrete details**: Use business-value numbers (接口数量、页面数、配置参数个数), NOT internal numbers (commit 数、PR 编号、test coverage)
6. **No markdown headers inside sections**: Use bold project names as line text, not `####` or `#####`
7. **Each project 1-2 bullets**: Compress into core deliverables, don't list every sub-task

## Style Reference — Boss-Readable Writing

The report is for a manager who does NOT read code. Write in **business language**:

- Explain **what was done** + **what it enables**, not how it was implemented
- Use domain terms the boss understands (接口、页面、配置参数、用户可以...)
- Do NOT use: technical jargon (Router Factory, Playwright E2E, migration downgrade), internal process names (CLAUDE.md, openspec review schema), version bumps (v0.2.0→v0.2.1), commit/PR counts, CI/CD details

### Good Examples

`**System 模块开发完成**：完成项目管理、成员管理、角色权限共 14 个后端接口，支持四级角色权限体系`

`**ha-dali-center v0.13.0 发布**：新增 4 个设备配置参数，用户可在 Home Assistant 中直接读写，无需依赖桌面软件。已完成端到端测试验证`

### Bad Examples

`完成了 auth 相关的工作` — too vague, no specifics

`重构了 BaseService 提取 UUID 解析和成员查询逻辑到基类减少 350 行代码` — too implementation-focused

`srhome-core 从 v0.1.0 发版到 v0.2.0（新增 INSTALLER 角色枚举）和 v0.2.1（中文 API 描述），sunlite / sylsmart submodule 同步升级` — internal version/infra details, boss doesn't care

`添加 Claude Code GitHub Workflow（PR#77），修复 fork PR 无法访问上游 secrets` — CI internals, skip entirely
