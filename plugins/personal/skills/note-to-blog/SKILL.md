---
name: note-to-blog
description: >-
  用于从 Obsidian 笔记库中筛选可发布内容，选择博客主题，或把已有笔记转换成博客草稿。
  用户提出「选一篇笔记发博客」「写博客」「博客选题」「从笔记里找文章」或
  "note to blog" 时立即使用。不用于从零撰写新文章、校对已有博客草稿或整理普通笔记。
---

# 笔记转博客

从 Obsidian Note 仓库中筛选适合发布的笔记，评估适配性，批量选题，双通道处理（快速转换 / 深度研究），并行 Agent 派发。

## 前置条件

| 工具 | 类型 | 必需 | 安装方式 |
|------|------|----------|---------|
| Python 3 | CLI | 是 | macOS 已预装 |
| PyYAML | CLI | 是 | `pip install pyyaml` |
| writing-assistant | skill | 否 | 由 `personal` plugin 提供 |

> 加载 skill 时不要主动检查这些工具。命令因缺少工具而失败时，再逐步引导完成安装和配置。

## 不适用情况

- 笔记库少于 5 篇时，手动选题更快
- 只想转换单篇已确定的笔记 — 直接运行 `<skill-dir>/scripts/note-to-blog.py convert "<path>"`
- 博客草稿已存在，只需校对 — 使用 `writing-assistant`

## 脚本位置

所有确定性操作均由 Python 脚本处理：

```text
<skill-dir>/scripts/note-to-blog.py  (collect / convert / state subcommands)
```

路径配置位于 [user-config.md](references/user-config.md)。以下 Bash 示例中的
`<PLACEHOLDER>` 需要替换为该配置文件中的值。

## 工作流概览

```text
步骤 1           步骤 2            步骤 3              步骤 4             步骤 5
 收集      ──▶   选择深度    ──▶   按深度处理    ──▶   执行         ──▶   汇总
 (script)        (user)            ├─ L1 浏览          (Agent Teams)       (report)
                                   ├─ L2 推荐
                                   └─ L3 深探
                                        │
                                   交互 ──▶ 分配处理通道 ──▶ 确认
```

## 步骤 1：收集候选笔记

使用 [user-config.md](references/user-config.md) 中的路径运行 `collect`：

```bash
python3 <skill-dir>/scripts/note-to-blog.py collect \
  --note-repo "<NOTE_REPO>" \
  --blog-content "<BLOG_CONTENT>" \
  --project-paths <PROJECT_PATHS> \
  --history-file "<HISTORY_FILE>"
```

脚本向标准输出写入一个 JSON 对象，包含：

- `candidates`：所有符合条件的笔记，包含 title、summary、char_count 和 outgoing_links
- `clusters`：具有 3 个以上入链的 wikilink 中心节点及相关笔记
- `published_posts`：现有博客文章的 title、tags 和 collection
- `session_keywords`：近期 Claude Code 会话的活动信号
- `stats`：total_scanned、filtered_out 和 candidates_count

读取 JSON 后进入步骤 2。

## 步骤 2：选择处理深度

展示数据规模并提供 Level 选项：

```text
collect 完成：
  候选笔记: {candidates_count} 篇 (总扫描 {total_scanned}, 过滤 {filtered_out})
  主题簇: {clusters_count} 个 (3+ 引用 hub)

可选深度:
  Level 1 浏览    直接展示候选列表，手动选择          0 额外 token
  Level 2 推荐    LLM 评估 + 主题簇分析              ~2k token     ← 推荐
  Level 3 深探    Level 2 + 读取 hub 笔记全文         ~5k+ token

选择 Level (1-3)?
```

### 深度速查

| Level | 名称 | 评估方式 | 后续流程 |
|:---:|:---|:---|:---|
| 1 | 浏览 | 无 LLM，候选按字数降序 | 用户直选 → 全部 fast track |
| 2 | 推荐 | LLM 评估摘要 + 主题簇 → 5-8 推荐 | fast/deep track 分配 |
| 3 | 深探 | Level 2 + 读取 hub 笔记全文 | fast/deep track，cluster 推荐更准确 |

### 推荐逻辑

| 候选数 | clusters | 推荐 |
|--------|----------|------|
| ≤ 10 | any | Level 1 |
| > 10 | 0 | Level 2 |
| > 10 | 1+ | Level 2 |

用户明确说「想发现主题」「有什么可以整合的」时 → 推荐 Level 3。

## 步骤 3：按深度处理

### Level 1：浏览

跳过 LLM 评估，按 char_count 降序展示候选项：

```text
#  标题                         字数    链接数
1  关于后LLM时代的代码Review     3200    5
2  SSH私钥加密                   1200    2
3  Feed内容阅读姿势              1800    3
...
```

用户按编号选择。Level 1 的所有选项只进入 **Fast track**，不提供 Deep track。

选择后直接进入「确认并执行」。

### Level 2：推荐

使用 [scoring-criteria.md](references/scoring-criteria.md) 中的提示模板执行一次 LLM 评估。

**输入**：使用 `collect` JSON 中的 candidates、clusters、published_posts 和
session_keywords 生成评估提示。

**输出**：LLM 必须返回包含 5～8 条推荐的 JSON 数组。完整格式见
[scoring-criteria.md](references/scoring-criteria.md)。

响应不是有效 JSON 时，补充明确的格式要求并重试一次。

评估完成后进入「交互选择」。

### Level 3：深度探索

处理方式与 Level 2 相同，但在调用 LLM 前，读取每个主题簇中心笔记的全文，并追加到评估提示中。

对 `collect` JSON 中 `hub_path` 不为空的每个 cluster：

1. 从 Note 仓库读取中心笔记全文。
2. 把全文追加到 LLM 提示的 `## Hub 笔记全文` 章节。Level 3 输入格式见
   [scoring-criteria.md](references/scoring-criteria.md)。

这样可以让 LLM 根据真实内容推荐主题簇，而不是只依赖元数据。

评估完成后进入「交互选择」。

## 交互选择（Level 2/3）

### 展示推荐

使用混合表格展示推荐列表：

```text
#  类型    标题                    适配分  目标   工作量  活跃   重复风险
1  单篇    后LLM时代代码Review      92    blog    小    ★★★    无
2  主题簇  优雅的哲学 (9篇关联)      88    blog    大    ★      无
3  单篇    SSH私钥加密              85    til     小    ─      无
...
```

### 用户操作

| 操作 | 示例 | 结果 |
|--------|---------|--------|
| 选择并分配通道 | "1 和 3 快速转换，2 走深度" | 按指定通道加入队列 |
| 覆盖 collection | "1 放 til" | 修改目标 collection |
| 批量跳过 | "4~6 跳过，reason: private" | 通过 `state skip` 标记为跳过 |
| 查看更多 | "还有别的吗" | 请求更多推荐 |
| 检查状态 | "状态" | 运行 `state status` |

**跳过时**立即运行：

```bash
python3 <skill-dir>/scripts/note-to-blog.py state skip "<path>" --reason "<reason>" \
  --note-repo "<NOTE_REPO>"
```

### 处理通道分配

| 通道 | 使用时机 | 处理方式 |
|-------|-------------|--------------|
| **Fast**（快速） | 独立且基本完整的笔记 | 脚本转换 → Agent 审校 → 草稿 |
| **Deep**（深度） | 需要调研的主题簇或粗略笔记 | Agent 读取所有相关笔记 → 调研报告 |

默认规则：`effort: "小"` 进入 Fast；`type: "cluster"` 或 `effort: "大"` 进入
Deep。最终由用户决定。

## 确认并执行

所有 Level 都需要展示确认摘要：

```text
确认选择：
  Fast track:
    1. 后LLM时代代码Review → blog/
    3. SSH私钥加密 → til/
  Deep track:
    2. 优雅的哲学 (9篇关联) → blog/

开始处理？
```

等待用户确认后再派发任务。

### 并行派发

使用 Task 工具并行派发 N 个 Agent，每个选中项对应一个任务。

> 其他 Agent 环境：以下 Fast/Deep track 任务相互独立，可按顺序依次执行。

```text
总编 (Main Agent)
├── Task Agent 1: 文章 A (fast track)
├── Task Agent 2: 文章 B (fast track)
└── Task Agent 3: 主题簇 C (deep track)
```

在一条消息中启动全部 Agent。每个 Agent 使用 `general-purpose` 类型，并在提示中提供完成任务所需的全部信息。

Fast Track 和 Deep Track 的完整 Agent 提示模板见
[agent-instructions.md](references/agent-instructions.md)。

### 状态更新

各 Agent 不直接更新 `.note-to-blog.json`。全部任务完成后，由主 Agent 依次更新状态：

```bash
python3 <skill-dir>/scripts/note-to-blog.py state draft "<note_path>" \
  --target "<collection>/<slug>.md" \
  --note-repo "<NOTE_REPO>"
```

Deep track 项目不标记为 drafted，等待用户进一步决定。

## 汇总结果

全部 Agent 完成后，展示统一摘要：

```text
Fast Track 完成：
  ✓ 后LLM时代代码Review → repos/bokushi/src/content/blog/llm-code-review.md
    - 转换正常，无问题
  ✓ SSH私钥加密 → repos/bokushi/src/content/til/ssh-key-encryption.md
    - 发现 1 个 TODO 标记需要手动处理

Deep Track 完成：
  📋 优雅的哲学 (9篇关联)
    - 研究报告已生成
    - 下一步？ a) 按大纲写作  b) 修改大纲  c) 暂不处理

状态更新：
  drafted: N 篇

草稿均为 hidden: true，需要手动 review 后改为 false 发布。
建议使用 `writing-assistant` 进行审校。

发布后运行:
  python3 <skill-dir>/scripts/note-to-blog.py state publish "<note_path>" --note-repo "<NOTE_REPO>"
```

## 详细参考

- 路径配置：[user-config.md](references/user-config.md)
- LLM 评估提示和评分规则：[scoring-criteria.md](references/scoring-criteria.md)
- Agent 提示模板：[agent-instructions.md](references/agent-instructions.md)
