# PR/MR description: prose-only schema

Date: 2026-04-25
Status: Draft (pending user review)
Owner: niracler
Affects skills: `git-workflow`, `yunxiao`

## Context

`git-workflow` skill 当前规定的 PR template 是两段式：

```markdown
## Summary
- bullet 1
- bullet 2
- bullet 3

## Test plan
- [ ] case 1
- [ ] case 2
```

实际 AI 生成的 MR 描述（包括云效平台上）出现「四轴 bloat」：

1. 信息密度低 — 把 diff 已经能说明的 what 在描述里再说一遍
2. 结构太重 — 出现「背景 / 动机 / 方案 / 影响 / 回滚」八股
3. 装饰元素花哨 — emoji 充当 bullet、四级 heading、表格充当 bullet
4. AI 生成味重 — 「本次变更主要包含」「值得注意的是」「综上所述」

reviewer 体验是「这是产品发布稿，不是 review 材料」。

问题不在某段细节，而在写作流派的选择。

## Decision

PR/MR 描述改用 **prose-only** 流派，对齐 cbeams + Google CL Descriptions
传统：

- subject = conventional commit（imperative，≤72 char）
- body = 2-3 句散文，回答 why（不重复 diff 已说明的 what）
- 末段 = 一行 `验证：xxx` 或 `Verify: xxx`
- **不使用任何 markdown section heading**（不要 `## Summary` `## Test plan`）

squash merge 时，PR 描述天然等于 squash commit message，避免「commit
message 写一份、PR 描述写一份、CHANGELOG 再写一份」的重复。

## Rationale

- **first line stand alone**：cbeams 与 Google CL Descriptions 都强调
  subject 必须独立可读、imperative。prose-only 把这条延伸到整体描述：
  body 也是给阅读者用的散文，不是给 template 填空。
- **没有 heading → AI 不会"为了模板而填空"**。`## Summary` 这种 heading
  本身是诱因——AI 看到 heading 会自动凑 3 条 bullet，即使没有 3 条
  独立信息。
- **PR ≠ RFC**。真正需要「背景 / 方案 / 影响 / 回滚」结构的场景，
  应该写 `openspec/changes/{change-id}/` 或 `docs/specs/`，PR 描述
  link 过去。两者读者不同（RFC 给设计阶段决策者，PR 描述给 review
  阶段 reviewer），保鲜期也不同（RFC 写一次，PR 描述跟着 git log 永久）。
- **squash commit message 与 PR 描述统一**：squash merge 后 PR 描述
  自动成为 main 分支上的 commit message。如果 PR 描述是 prose，
  这条 commit message 也就是 prose；reviewer 阅读体验和 git log
  阅读体验合一。

## Schema

```text
<type>(<scope>): <imperative subject>      ← title，≤72 char

<2-3 句 prose 解释 why。中文用全角标点，英文用半角；
不要 bullet list 复述 commit。>

<可选：1 句指点 reviewer 重点关注的位置>

验证：<一行说怎么自测的，或 N/A: docs only>
```

字段说明：

- **subject**：沿用 `git-workflow` skill 现行 conventional commits
  规则（type、scope、imperative、≤72 char、不以句号结尾），无变化。
- **body**：≤3 段、≤200 字（中文）或 ≤120 words（英文）。回答
  「为什么改 / 为什么这样改 / 已知不完美的地方」。
- **reviewer hint（可选）**：当 diff 很大或重点不明显时，用一句话
  指点（"重点看 `src/sdk/device.py` 的 listener 注册顺序"）。可省。
- **验证 / Verify**：必填一行，说明如何自测；docs-only / config-only
  PR 写 `验证：N/A: docs only` 显式声明而非省略。

## Forbidden patterns

明确禁止：

1. Markdown section heading：`##`、`###`、`####`
2. emoji 充当 bullet 或 heading：🔧 ✅ 💡 ⚡ 🚀 📝
3. commit message 列表 / 文件清单 / 改了几行的统计 — diff 已说明
4. AI 套话：「本次变更主要包含」「值得注意的是」「综上所述」
   「希望对你有帮助」「为了更好地」
5. 折叠块（`<details>`）/ 表格充当 bullet
6. 反思叙事体（"我考虑过 A 也考虑过 B 但最后……"）— 技术 prose
   应该是 declarative impersonal（"旧固件 X，所以在这里 Y"），
   不是过程回忆录。设计权衡写到 `docs/specs/` 或 `openspec/changes/` 里

## Allowed but capped

- 链接：可以放，用裸 URL 或 `[text](url)`，不用 reference-style
- 行内代码：允许 `` `func_name` ``、`` `--flag` ``、`` `path/to/file.py` ``
- bullet list：仅当列举多个独立 verify 步骤时允许（验证段内），
  body 里禁止
- 表格：禁止
- 截图：仅 UI 类改动允许，且单 PR ≤2 张

## Examples

### 中文示例 — 小修复

```text
fix(sensor): clamp energy reading at 65535

旧固件在 power > 65W 时把 wh 字段回卷到 0，触发 HA 历史
图断点。在 device 层 clamp，避免上层每个 entity 各自防御。
不改 SDK 接口。

验证：手工喂 wh=70000，HA 显示 65535 而不是 0。
```

### 英文示例 — 重构

```text
refactor: move register_listener to entity objects

The old global gateway listener forced every integration entity
to import the gateway singleton, which broke unit tests that
spin up devices in isolation. Move register_listener() onto
Device/Group/Scene so entities own their own subscription.

Reviewer hint: src/sdk/device.py is the new home; old gateway.py
becomes a thin wrapper.

Verify: pytest tests/unit/test_device_listener.py
```

### Docs-only 示例

```text
docs(skill): switch yunxiao MR examples to prose-only

git-workflow 切到 prose-only 之后，yunxiao references/openapi.md
里的 ## Summary 示例还在引导 AI 走旧模板。同步替换。

验证：N/A: docs only。
```

## File changes

| 文件 | 改动 |
|------|------|
| `skills/workflow/git-workflow/SKILL.md` | 在 "Default Behaviors" 加 PR description prose-only 子节，引用新示例 |
| `skills/workflow/git-workflow/references/examples-and-templates.md` | 删除 `## PR Template` markdown 模板，替换为 prose schema + 上述三个示例 + forbidden patterns 列表 |
| `skills/workflow/yunxiao/references/openapi.md` | 行 158、249 的 `## Summary\n\n- Change 1` 示例改为 prose 单段 |
| `CHANGELOG.md` | `## [Unreleased]` 下 `### Changed` 加一条 `git-workflow — switch PR description to prose-only schema` |

不动：

- `scripts/validate_commit.py` — 仍然只校验 commit message（PR 描述
  自动化校验难度高，靠 AI 自检 + 人工 review 即可）
- 其他 skill 的 commit / release 流程

## Out of scope

- 不动 commit message 规范（仍是 conventional commits）
- 不动 release / CHANGELOG 流程
- 不引入 PR description validator script
- 不强制 niracler 之外的人遵守 — 这是个人 skill repo 偏好

## Open questions

无。Prose-only 方向已确认，细节按合理推论填充，欢迎在 spec review
阶段批改。
