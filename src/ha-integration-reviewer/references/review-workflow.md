# HA 集成审查工作流

并行审查策略，使用多个检查维度同时进行。

## 并行检查架构

使用 Task 工具启动多个 subagent 并行检查：

```text
┌─────────────────────────────────────────────────────────────┐
│                    主审查流程                                │
├─────────────────────────────────────────────────────────────┤
│  1. 收集待审查文件（git diff / 指定目录）                     │
│  2. 并行启动 4-5 个专项检查 agent                            │
│  3. 汇总各 agent 结果                                        │
│  4. 生成统一审查报告                                         │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌────────┬────────┬────────┬────────┬────────┐
│ Agent1 │ Agent2 │ Agent3 │ Agent4 │ Agent5 │
│ Quality│ Code   │ Config │ Test   │ Doc    │
│ Scale  │ Style  │ Flow   │Coverage│ Check  │
└────────┴────────┴────────┴────────┴────────┘
```

## 检查维度详解

### Agent 1: Quality Scale 规则检查

**任务**: 验证 quality_scale.yaml 中的规则状态

**工作流**:

1. 读取 `quality_scale.yaml` 获取当前规则状态
2. 对于每个 `done` 状态的规则:
   - 从 GitHub 获取规则文档: `https://raw.githubusercontent.com/home-assistant/developers.home-assistant/refs/heads/master/docs/core/integration-quality-scale/rules/{rule_name}.md`
   - 验证代码是否符合规则要求
3. 对于每个 `todo` 状态的规则:
   - 检查是否接近完成（可以提示用户考虑完成）
4. 对于每个 `exempt` 状态的规则:
   - 验证豁免理由是否合理

**输出**: 规则合规报告

### Agent 2: 代码风格检查

**任务**: 检查 copilot-instructions.md 中的编码规范

**检查项**:

- 异步编程规范（所有外部 I/O 必须 async）
- 异常处理模式
- 日志规范
- 类型注解完整性
- Python 3.13+ 语法偏好

**参考**:

- [copilot-instructions.md](https://github.com/home-assistant/core/blob/dev/.github/copilot-instructions.md)
- [references/common-issues.md](common-issues.md)

### Agent 3: Config Flow 检查

**任务**: 验证配置流程实现

**检查项**:

- unique_id 正确设置
- 错误处理类型正确（ConfigEntryNotReady / ConfigEntryAuthFailed / ConfigEntryError）
- runtime_data 使用规范
- 测试覆盖率 100%
- UI 文本规范

### Agent 4: 测试覆盖检查

**任务**: 验证测试完整性

**检查项**:

- 测试文件存在于 `tests/components/{domain}/`
- 使用 snapshot testing
- 使用 fixture 而非直接访问 `hass.data`
- Mock API 响应来自 JSON fixtures
- 覆盖率 >= 95%

### Agent 5: 文档与 Manifest 检查

**任务**: 验证元数据和文档

**检查项**:

- manifest.json 完整性
- strings.json 翻译完整
- 敏感数据使用 `async_redact_data()` 处理
- Repair issues 有可操作的步骤

## 动态文档获取

使用以下方式获取最新文档，而非静态嵌入：

### WebFetch

```python
# 获取 quality scale 规则
url = f"https://raw.githubusercontent.com/home-assistant/developers.home-assistant/refs/heads/master/docs/core/integration-quality-scale/rules/{rule_name}.md"

# 获取 copilot-instructions
url = "https://raw.githubusercontent.com/home-assistant/core/dev/.github/copilot-instructions.md"
```

### Context7

用于获取 Home Assistant 开发者文档的最新内容：

- Review process
- Development checklist
- Integration quality scale

### 参考其他集成

从 ha-core 仓库查看类似集成的实现：

```bash
# 搜索类似模式
gh api repos/home-assistant/core/contents/homeassistant/components/{similar_integration}
```

## 报告格式

```markdown
# HA 集成审查报告

## 概要
- 检查时间: {timestamp}
- 检查范围: {files}
- 总体状态: {PASS/NEEDS_WORK}

## Quality Scale 检查
### Done 规则验证
- [x] {rule}: 符合要求
- [ ] {rule}: 不符合 - {原因}

### Todo 规则（接近完成）
- {rule}: {距离完成的差距}

### Exempt 规则审查
- {rule}: {豁免理由评估}

## 代码风格
- [ ] {issue}: {file}:{line} - {description}

## Config Flow
- [ ] {issue}: {description}

## 测试覆盖
- 当前覆盖率: {percentage}%
- 缺失测试: {list}

## 文档
- [ ] {issue}: {description}

## 建议的修复优先级
1. {high_priority_fix}
2. {medium_priority_fix}
...
```
