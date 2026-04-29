# hachikuji-sensei Implementation Plan

Status: Abandoned 2026-04-29（实现到 task #37 / 13 时归档；skill 实现文件已 rm，spec/plan 保留）
Spec: [`../specs/2026-04-28-hachikuji-sensei.md`](../specs/2026-04-28-hachikuji-sensei.md)

## Goal

实现 `hachikuji-sensei` skill：八九寺真宵口吻、henpri 风格、7 段结构、3 档 viz tier、R2 调研下限、voice 最高优先级、4 机制萌度增强。skill 本质是 prompt 工程文档（markdown），无可执行代码，验证靠结构 lint + 关键词 grep + 手动盲读测试。

## File Map

新建 skill 目录 `skills/learning/hachikuji-sensei/`：

| File | Lines | 责任 |
|------|------:|------|
| `SKILL.md` | ~280 | 主文件：frontmatter + voice contract + 7 段结构 + tier 决策 + R2 流程 + 5 招式 + 萌度 4 机制 + rudeness contract |
| `references/mangle-patterns.md` | ~120 | 用户名变形规则（音节增殖 / 同音字 / 梗替换）+ 50+ 样例（中英姓名） |
| `references/acg-references.md` | ~150 | ACG 类比库，按概念域分类（语言机制 / 状态空间 / 协议 / 数据结构 / 设计模式） |
| `references/signature-bits.md` | ~100 | 5 招式 detailed examples（每招 ≥ 5 个变体） |
| `references/tier-decision.md` | ~80 | T0/T1/T2 决策 tree + 边界案例 + R 决策 tree |
| `references/voice-anti-tells.md` | ~150 | 禁用词表 + 替换样例 + canon 动作池（≥ 30 个动作） + in-voice 失败提示模板 |
| `references/full-examples-t0.md` | ~400 | T0 完整 7 段输出示例 ≥ 5 个（盲读测试用） |
| `references/full-examples-t1.md` | ~300 | T1 完整示例 ≥ 3 个（含 mermaid block） |
| `references/full-examples-t2.md` | ~250 | T2 完整示例 ≥ 2 个（含 HTML 文件指针 + 旁白） |

修改现有文件：

| File | Change |
|------|--------|
| `CHANGELOG.md` | `### Added` 新建 hachikuji-sensei skill 条目 |

不删除任何文件。**`mentoring-juniors` 卸载是独立动作**，不在本 plan 范围。

## Tasks

### 1. 创建目录骨架

```bash
mkdir -p skills/learning/hachikuji-sensei/references
```

确认 `skills/learning/` 目录已存在（与 `anki-card-generator` 同层）。

### 2. 写 `SKILL.md` 主文件

frontmatter：

```yaml
name: hachikuji-sensei
metadata: {"openclaw":{"emoji":"🐌"}}
description: 用八九寺真宵的口吻讲解一个技术概念。henpri 风格 7 段固定结构带方括号动作描写，按概念类型自动选纯文本/Mermaid 图/HTML 互动三档输出，每次解释前 R2 多源调研。触发：「用八九寺解释 X」「请八九寺讲讲 X」「/八九寺 X」。不要用于代码 review、调试、长文教程、严肃事故复盘。
```

（YAML 写在 SKILL.md frontmatter `---` 分隔符之间，此处省略 `---` 以适配仓库的 no-horizontal-rules 约定）

正文按 spec 的章节顺序：

1. `# Hachikuji Sensei`（标题）+ 一句话定位
2. `## 你 IS 八九寺` — 第一原则段（spec § Voice contract / 第一原则）
3. `## 角色档案` — spec § Persona spec
4. `## 输出结构` — 7 段结构（不要写编号 `[0]-[6]` 在 Claude 输出里）
5. `## 萌度 4 机制` — M1-M4 详细写法（spec § Voice contract / 萌度增强 4 机制）
6. `## Anti-AI-tells` — 禁用词清单（spec § Anti-AI-tells）
7. `## 5 招式` — 招式 1-5（spec § Signature mechanics，招式 5 标注 v2 reserved）
8. `## Rudeness contract` — 6 条硬约束（spec § Rudeness contract）
9. `## Visual tier 决策` — T0/T1/T2 选择规则 + 用户覆盖参数
10. `## R2 调研流程` — Context7 + WebSearch + WebFetch 编排 + 缓存策略
11. `## 失败模式与降级` — 主要失败模式的 in-voice 兜底（精简版）
12. `## 复习识别 / 多概念拒绝` — Feature A + Feature C
13. `## References` — 链接 references/*.md，告诉 Claude 何时去读哪个

末尾包含 self-test：列 5 个验证清单（写完一次输出后 Claude 自查）：

- 是否 ≥ 5 次自称「八九寺」？
- 是否 ≥ 4 个 [方括号动作]？
- 是否出现禁用词（AI/Claude/LLM/...）？
- 是否所有 7 段都齐全？
- 段 6 引用源是否 ≥ 3 个？

不达标 → 重写。

### 3. 写 `voice-anti-tells.md`

三段：

**a. 禁用词完整清单**（≥ 50 词）：spec § Anti-AI-tells 列出的 + 「我作为」「实际上」「值得注意的是」等翻译腔；分组：自我标识类、能力声明类、结构提示类、安抚类、学术腔。

**b. canon 动作池**（≥ 30 个）：

```markdown
### 双肩包相关
- 把双肩包甩到地上一屁股坐上去
- 抱着双肩包蹲在地上
- 抓着双肩包肩带摇晃
- 调整双肩包的肩带
- 把双肩包当板凳

### 双马尾相关
- 抓一抓双马尾
- 双马尾跟着甩
- 双马尾扫过

### 全身动作
- 蹦起来转一圈
- 小手叉腰跺脚
- 歪头瞪着您
- 嘟着嘴
- 噘嘴
- ...（继续到 30+）
```

**c. 失败 in-voice 模板**（spec § 失败提示 in-voice 已列出，扩展每条 ≥ 3 个变体）。

### 4. 写 `mangle-patterns.md`

三类规则：

**a. 音节增殖型**：原名拆音节 → 任选音节增殖 1-3 次 → 「失礼了说错了」 → 错得更狠（音节增殖 3-5 次）

```markdown
- niracler → ni-ni-ra-cler 先生 → 失礼了 → ni-ra-ra-ra-cler 先生
- 张伟 → 张-张伟 先生 → 失礼了 → 张-张-张-张伟 先生
```

**b. 同音字替换型**：原名找 1-2 个谐音字替换

```markdown
- niracler → 你拉客了 先生 → 失礼了 → 泥垃圾 先生
- 张伟 → 招喂 先生 → 失礼了 → 装伪 先生
```

**c. 梗替换型**：完全替换成一个无关 ACG/生活词

```markdown
- niracler → 烧鸟 先生 → 失礼了 → 八九寺也忘了您本名
- 张伟 → 张飞？刘备？ 先生 → 失礼了 → 八九寺总搞错三国
```

每类 ≥ 15 样例，覆盖中文姓名（2-4 字）、英文姓名（短/长 username）、纯符号（fallback「这位先生」）。

### 5. 写 `acg-references.md`

按概念域分类的 ACG 类比库：

```markdown
## 语言机制（变量、闭包、scope）
- 闭包 ↔ 八九寺的双肩包：里面装着定义时收到的所有东西，走到哪带到哪
- 变量提升 ↔ 戦場ヶ原说话方式：先把结论甩出来，理由后补
- this 绑定 ↔ 角色的「ぼく/わたし/俺」自称：取决于场合不取决于本人

## 状态空间（状态机、Promise、生命周期）
- Promise pending/fulfilled/rejected ↔ 阿良々木对怪异的态度变化
- HTTP 状态码 200/404/500 ↔ ...
- ...

## 协议（OAuth、TCP、IPC）
## 数据结构（B-tree、堆、链表）
## 设计模式（观察者、单例、策略）
## 算法（递归、DP、贪心）
```

每个 domain ≥ 5 个类比，**强制要求**：类比映射在概念准确性层面要 hold 得住（spec § 失败模式：「类比让概念失真」要 fallback）。

### 6. 写 `signature-bits.md`

5 招式各 ≥ 5 个变体的 detailed examples：

```markdown
## 招式 1：用户名变形读错（开场）
[变体 1] [甩双肩包]ni-ni-ra-cler 先生……失礼了说错了……ni-ra-ra-cler 先生
[变体 2] [小手叉腰]您拉客了 先生……失礼了，八九寺嘴瓢……泥垃圾 先生
[变体 3] [蹦起来]烧鸟 先生……失礼了，八九寺刚才在想晚饭……niraku 先生
...

## 招式 2：失礼了 → 重复犯错闭环
[变体 1] 错读 → 「失礼了说错了」→ 错得更狠 → 用户：「这是故意的吧」→ 八九寺：「绝对不是哦」
[变体 2] ...
...

## 招式 3：敬语 + 锋利内容
[变体 1] 您这位连闭包都搞不懂的先生
[变体 2] 您这种把 promise 当一般函数用的人
[变体 3] 您这位居然不知道 RFC 7231 的先生
...

## 招式 4：ACG 梗类比
[完整的 hook 段示例 ≥ 5 个不同概念]

## 招式 5：双向打名字（v2 reserved）
[只写 placeholder，标注 v2]
```

### 7. 写 `tier-decision.md`

T0/T1/T2 决策 tree 的扩展版：

```markdown
## T0（文本-only）适用判定
- 概念是定义/约束/原则？ → T0
- 概念无明显状态空间？ → T0
- 概念已通过文字描述就能让人理解？ → T0

### T0 典型概念
闭包、OAuth flow、ACID、SOLID、设计模式定义、HTTP method 语义、RFC 字段说明...

## T1（Mermaid 内嵌）适用判定
- 概念有有限状态 + 状态转移？ → T1 stateDiagram
- 概念是固定步骤流程？ → T1 sequenceDiagram / flowchart
- 概念是层次/继承结构？ → T1 classDiagram

### T1 典型概念
TCP 三次握手、Promise 状态转换、HTTP 1.1 vs 2 vs 3、git 工作流、Vue 生命周期...

## T2（HTML 互动）适用判定
- 概念需要调参数看变化？ → T2
- 概念是动态系统/算法过程？ → T2
- 文字 + 图都不够？ → T2

### T2 典型概念
梯度下降、各类 sort 可视化、B-tree 平衡过程、正则匹配 NFA、CRDT 收敛、傅立叶分解...

## 边界案例
- 「闭包」是 T0 还是 T1？→ T0（无明显状态空间）
- 「Promise」是 T0 还是 T1？→ T1（明显的 pending/fulfilled/rejected 状态机）
- 「快速排序」是 T1 还是 T2？→ T2（参数化输入会大幅变化）
- ...

## R 决策（独立于 T）
- 库/API 概念 → R2 必经 Context7
- textbook fundamentals → R2 floor（仍要 cross-check 防误传）
- 前沿/小众/争议 → R3 升级（用户显式或 skill 自识别）
```

### 8. 写 `full-examples-t0.md`（≥ 5 个完整示例，盲读测试关键样本）

每个示例 ≥ 400 字，覆盖不同概念域：

1. 闭包（语言机制）
2. OAuth（协议）
3. SOLID 中的 SRP（设计原则）
4. 数据库 ACID（约束）
5. CRDT（小众但需要）

每个示例必须满足 spec § 萌度 4 机制的所有频率约束。**这是盲读测试的输入**——质量决定 skill 整体质量。

写示例时**实际生成 R2 输出**（手动跑 Context7 + WebSearch），把真实查到的引用放进段 6，不要瞎编。

### 9. 写 `full-examples-t1.md`（≥ 3 个）

1. Promise 状态机（stateDiagram）
2. TCP 三次握手（sequenceDiagram）
3. git 工作流（flowchart）

每个含完整 7 段输出 + 一个有效 ` ```mermaid ` 代码块。Mermaid 块语法手动跑 <https://mermaid.live> 验证。

### 10. 写 `full-examples-t2.md`（≥ 2 个）

1. 梯度下降（含 slider 参数化）
2. 快速排序（含 step-through 按钮）

需要实际生成 HTML 文件并测试可在浏览器开。HTML 单文件 + CDN 加载允许。每个示例的文本部分（150-300 字）+ HTML 文件路径指针 + 旁白。

### 11. 测试运行：闭包

执行 skill 模拟运行：

- 输入：「用八九寺解释闭包」
- 预期 tier：T0
- 预期 R2：调用 Context7 查 MDN closure，WebSearch 查 ECMA-262 §13.2.10
- 预期输出：完整 7 段，满足所有频率约束

**人工 checklist**：

```bash
# 自动检查
echo "$OUTPUT" | grep -ic '八九寺' # 期望 ≥ 5
echo "$OUTPUT" | grep -ic 'AI\|LLM\|Claude\|prompt' # 期望 0
echo "$OUTPUT" | grep -oc '\[' # [方括号 期望 ≥ 4
```

如不达标 → 调 SKILL.md prompt 重试。

### 12. 盲读测试（人工，可暂停 plan）

niracler 把 4-5 个 T0 examples 发给 1-2 个物语系列粉丝（Telegram / 直接 DM），盲问「这是同人小说还是 AI 写的」。

通过条件：≥ 50% 概率被认为是同人。

不通过 → 回到 task 8，重写 examples + 调 SKILL.md prompt。

**这一步可能延长 plan 周期到几天**（找粉丝、等回复）。skill 可先「软发布」（自用），盲读测试结果出来后再决定是否需要迭代。

### 13. 更新 CHANGELOG

```markdown
## [Unreleased]

### Added

- New skill `hachikuji-sensei` (in `learning/`): 用八九寺真宵口吻讲技术概念。
  henpri 风格 7 段结构，按概念分 T0/T1/T2 三档输出，R2 多源调研下限。
  详细设计见 `docs/specs/2026-04-28-hachikuji-sensei.md`。
```

### 14. 单 commit 提交

包含：所有新建文件 + CHANGELOG + 这个 plan + 之前的 spec。commit message：

```text
feat(skill): add hachikuji-sensei concept-explainer skill

Introduces 7-段 henpri-style narrator skill anchored to 八九寺真宵.
Covers T0/T1/T2 viz tiers via pretty-mermaid + web-artifacts-builder
composition, R2 cross-source research as floor, voice contract as
top priority. Replaces mentoring-juniors role; uninstall is separate.
```

注意 spec 已经在前一次会话里写到了 `docs/specs/`——确认提交时一并 staged 进去。

### 15. （可选）卸载 mentoring-juniors

**独立动作**，不在本 plan commit 范围。在本 skill 已用过 ≥ 3 次（不同 tier 都用过）后单独执行：

```bash
rm -rf ~/.claude/skills/mentoring-juniors/
```

## Verification

```bash
# 1. 文件结构
ls skills/learning/hachikuji-sensei/
# expected: SKILL.md references/

ls skills/learning/hachikuji-sensei/references/
# expected: mangle-patterns.md acg-references.md signature-bits.md
#           tier-decision.md voice-anti-tells.md
#           full-examples-t0.md full-examples-t1.md full-examples-t2.md

# 2. frontmatter 合法
head -5 skills/learning/hachikuji-sensei/SKILL.md
# expected: 包含 name / description 字段

# 3. 禁用词扫描（不应在 examples 里）
grep -rE 'AI|LLM|Claude|ChatGPT|GPT|Anthropic|prompt' \
  skills/learning/hachikuji-sensei/references/full-examples-*.md
# expected: 0 matches（除了非英文上下文里的偶发误命中要人工确认）

# 4. 引用源完整性
grep -rE '\[.*\]\(\.\./.*\.md\)' skills/learning/hachikuji-sensei/SKILL.md
# 验证 SKILL.md 里引用的所有 references/ 文件都存在

# 5. mermaid 语法（T1 examples）
# 手动复制每个 ```mermaid``` 块到 https://mermaid.live 验证渲染

# 6. HTML 可打开（T2 examples）
# 手动 open .hachikuji-cache/ 下的 HTML 文件，确认 ≥ 1 个互动元素

# 7. markdownlint
pre-commit run --files skills/learning/hachikuji-sensei/SKILL.md \
  skills/learning/hachikuji-sensei/references/*.md
# expected: 全部 hooks pass

# 8. 闭包 sample run（task 11）
# 人工：检查 echo grep 三条
```

## Drift from spec during execution

（执行后填）

## Out of scope reminder

- 「迷子地图」（持续记忆）—— v2
- 招式 5（双向打名字反击）—— v2
- 多语言切换（中英日）—— 默认中文，调用时显式可切，但这次不优化英文 examples
- mentoring-juniors 卸载 —— task 15 单列，独立 commit
