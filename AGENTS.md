# Niracler Skills 仓库约定

本文件只记录此仓库特有的结构、发布和内容约束。通用 Skill 质量规则由
`plugins/developer-workflows/skills/skill-reviewer/` 维护，不在此重复。

## 发布结构

- 已发布插件位于 `plugins/<plugin>/`，插件清单位于 `.agents/plugins/marketplace.json`。
- 插件清单固定为 `plugins/<plugin>/.codex-plugin/plugin.json`，Skill 固定为
  `plugins/<plugin>/skills/<skill>/SKILL.md`。
- 根目录 `.codex-plugin/` 和 `skills/` 属于已删除的聚合布局，不得重新创建。
- 插件名必须与目录名、Marketplace 条目和插件清单一致；Skill 名称在整个仓库中保持唯一。
- 新增、移动或删除插件与 Skill 时，按影响范围同步更新 Marketplace、插件清单、README 和
  `tests/test_plugin_contract.py`，避免发布内容与契约测试不一致。

## Personal 插件

- `plugins/personal/` 面向作者的中文工作流；`SKILL.md` 的触发描述、标题和自然语言说明以
  中文为主，相关模板与示例保持同一语言。
- 命令、路径、产品名、API 字段和其他机器可读内容保持原样。
- 轮班周期、日历名称、排期时段、数据源命令等运行规则写入对应 `SKILL.md` 或
  `references/`，不写入本文件。
- Personal 插件可以记录稳定且有意公开的个人偏好和 Obsidian 结构，但不得包含真实公司名、
  工作项目名、人员信息、内部主机名、公司仓库路径、访问令牌或原始工作数据。
- 示例使用「项目 A」「仓库 B」「成员 C」等匿名名称。远程工具的原始响应不得写入仓库。

## 文档同步

- README 的插件列表、Skill 列表和依赖说明应与当前目录及各 `SKILL.md` 保持一致。
- 对外可见的插件或 Skill 变化记录到 `CHANGELOG.md` 的 `Unreleased`，并归入 `Added`、
  `Changed`、`Fixed` 或 `Removed`。
- 仓库说明使用公开、可复用的信息，不把临时迁移过程或单次任务背景写成长期约定。

## 仓库验证

常规变更运行：

```bash
bash scripts/validate.sh
npx markdownlint-cli2 "**/*.md" "#repos" "#node_modules"
bash scripts/check-horizontal-rules.sh $(find . -name '*.md' -not -path './repos/*' -not -path './node_modules/*')
```

修改 Skill 发现或同步逻辑时，额外运行：

```bash
./scripts/sync --dry-run
npx skills add . --list --full-depth
```
