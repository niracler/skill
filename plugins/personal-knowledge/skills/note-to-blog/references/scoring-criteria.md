# Scoring Criteria

LLM evaluation prompt template and scoring rules for note-to-blog.

## Prompt Template

Use the following prompt for the single-call LLM evaluation (Level 2 and Level 3):

````markdown
你是一个博客选题顾问。根据以下候选笔记、主题簇、已发布博文和近期活跃信号，推荐 5~8 条最适合发布为博客的选题。推荐可以是单篇笔记（type: single）或主题簇（type: cluster）的混合。

## 候选笔记

{candidate_list}

## 主题簇（wikilink 关联发现）

{cluster_list}

## 已发布博文

{published_list}

## 近期活跃信号（最近 30 天）

{session_keywords}

## 评分维度

对每篇候选笔记按以下 4 个维度评分（各 25 分，满分 100）：

1. **完成度**（25 分）：内容是否足够完整，能否作为独立文章发布？
   - 25: 结构完整，有开头/正文/结尾，可直接发布
   - 15-20: 主体内容完整，需要少量补充
   - 5-10: 只有大纲或碎片化笔记
   - 0: 几乎空白或只有标题

2. **独特性**（25 分）：与已发布博文相比是否有新视角？
   - 25: 全新主题，已发布列表中无类似内容
   - 15-20: 相关主题存在但角度不同
   - 5-10: 与已发布内容高度重叠
   - 0: 几乎是已发布文章的重复

3. **时效性**（25 分）：是否与近期兴趣或当下热点相关？
   - 25: 与近期活跃信号高度匹配（3+ 关键词匹配）
   - 15-20: 部分匹配近期活跃信号
   - 10: 常青内容，无时效要求
   - 5: 内容可能已过时

4. **结构性**（25 分）：内容的可读性和结构化程度
   - 25: 有清晰的标题层级、段落分明、有代码/图片等素材
   - 15-20: 结构基本清晰，需要少量整理
   - 5-10: 流水账或缺乏结构
   - 0: 纯粹的信息堆砌

## 主题簇评估维度

对主题簇（type: cluster）使用不同的评分维度（各 25 分，满分 100）：

1. **主题深度**（25 分）：多篇笔记是否围绕有意义的核心主题？
   - 25: 明确的核心主题，多篇笔记从不同角度深入探讨
   - 15-20: 有共同主题但关联松散
   - 5-10: 仅因引用同一篇笔记而关联，实际主题分散
   - 0: 纯粹的结构性引用（如日记引用模板）

2. **素材充足度**（25 分）：关联笔记的内容量是否足以支撑一篇博文？
   - 25: 总字数 5000+ 且有实质内容，足以整合为完整文章
   - 15-20: 总字数 2000-5000，需要适量补充
   - 5-10: 内容碎片化，需要大量补充
   - 0: 几乎空白

3. **独特性**（25 分）：同单篇评估规则
4. **时效性**（25 分）：同单篇评估规则

## Session 活跃度加分规则

基于活跃信号中的关键词匹配数，标注活跃度等级：

| 匹配数 | 等级 | 说明 |
|--------|------|------|
| 3+ | ★★★ | 近期高度关注 |
| 1-2 | ★ | 有一定关联 |
| 0 | ─ | 无近期活跃信号 |

活跃度不直接加分到总分，而是作为"时效性"维度的重要参考信号。

## Collection 判断规则

根据候选笔记的内容特征判断最适合的目标 collection：

| 类型 | 特征 | 目标 |
|------|------|------|
| 技术笔记 | 教程、TIL、配置指南、单一技术点、操作步骤 | `til` |
| 长文随笔 | 观点文章、评论、生活感悟、作品评测、多角度讨论 | `blog` |
| 周/月记 | 时间段的生活记录、月度复盘、年度总结 | `monthly` |

## 重复风险判断

对比候选笔记和已发布博文：

| 情况 | duplicate_risk | 处理 |
|------|---------------|------|
| 标题和主题完全不同 | `none` | 正常推荐 |
| 相同主题但不同角度 | `low` | 推荐，并在 reason 中说明差异 |
| 高度相似或明显是已发布文章的来源 | `high` | 不推荐，或标注为 "可作为更新版" |
| 标题含 "2.0" "v2" 等更新标志 | `update` | 推荐，标注为已有文章的更新版 |

## 工作量估算

| 等级 | 含义 |
|------|------|
| 小 | 格式转换 + 基本修复即可，无需大量改写 |
| 中 | 需要补充部分内容或重新组织结构 |
| 大 | 需要大量改写、补充素材或重新构思 |

## 输出格式

返回 JSON 数组，按 score 降序排列。每条推荐须标注 `type` 字段（`single` 或 `cluster`）：

```json
[
  {
    "type": "single",
    "path": "Areas/大模型(LLM)/关于后 LLM 时代的代码 Review 的看法.md",
    "title": "关于后 LLM 时代的代码 Review 的看法",
    "score": 92,
    "collection": "blog",
    "effort": "小",
    "session_activity": "★★★",
    "duplicate_risk": "none",
    "reason": "结构完整、有真实案例、观点独特，且近期 session 高度活跃"
  },
  {
    "type": "cluster",
    "hub_title": "优雅的哲学",
    "hub_path": "Areas/生活(Life)/优雅的哲学-v2.0.md",
    "related_count": 9,
    "score": 88,
    "collection": "blog",
    "effort": "大",
    "session_activity": "★",
    "duplicate_risk": "none",
    "theme_summary": "关于如何优雅地生活的哲学思考，散落在多篇笔记中",
    "reason": "主题深度足够，需要整合多篇笔记"
  }
]
```

- `single` 类型：必须包含 path, title, score, collection, effort, session_activity, duplicate_risk, reason
- `cluster` 类型：必须包含 hub_title, hub_path, related_count, score, collection, effort, session_activity, duplicate_risk, theme_summary, reason
- score 为整数 0-100。返回 5~8 条推荐，单篇和主题簇混排。
````

## Level 3: Hub Note Full Text Input

When running at Level 3 (Deep Explore), append the following section to the prompt **after** `{cluster_list}` and **before** `## 已发布博文`:

````markdown
## Hub 笔记全文（Level 3 深探模式）

以下是各主题簇 hub 笔记的完整内容，供更准确的主题评估：

### {hub_title}

{hub_note_full_text}

### {hub_title_2}

{hub_note_full_text_2}
````

Only include hub notes where `hub_path` is not null. If a hub note cannot be read (file missing or encoding error), skip it silently and note in the prompt that the content was unavailable.

This additional context allows more accurate scoring of:

- **主题深度**: LLM can assess the actual depth of the hub note, not just link count
- **素材充足度**: LLM can gauge real content volume and quality
- **建议大纲**: LLM can suggest more concrete outlines based on actual content

## Input Format

### candidate_list

Each candidate is formatted as:

```yaml
- path: Areas/网络安全(Cyber Security)/SSH私钥加密.md
  title: 用三分钟对你个人电脑上的 SSH 私钥进行加密吧
  char_count: 1200
  summary: |
    SSH 私钥是你登录服务器的钥匙...
    (first 20 non-empty, non-frontmatter lines)
```

### cluster_list

Each cluster is formatted as:

```yaml
- hub_title: 优雅的哲学-v2.0
  hub_path: Areas/生活(Life)/优雅的哲学-v2.0.md
  link_count: 9
  related:
    - Areas/生活(Life)/思考、创作与反思.md
    - Areas/杂谈(Essay)/关于我.md
```

### published_list

Each published post is formatted as:

```yaml
- title: SSH Key Management Best Practices
  tags: [SSH, Security]
  collection: til
```

### session_keywords

A flat list of extracted keywords/summaries:

```yaml
- "LLM code review workflow discussion"
- "bokushi blog deployment fix"
- "SSH key rotation automation"
```
