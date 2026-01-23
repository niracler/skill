# HA 集成常见审查问题

来自真实 PR Review 的常见问题模式，作为快速检查清单。

> **参考来源**:
>
> - [PR #151479 Review](https://github.com/home-assistant/core/pull/151479) - Add DALI Center integration
> - [PR #159579 Review](https://github.com/home-assistant/core/pull/159579) - Add sensor platform support
> - [PR #159576 Review](https://github.com/home-assistant/core/pull/159576) - Upgrade to silver quality scale
> - [PR #161415 Review](https://github.com/home-assistant/core/pull/161415) - Add energy sensor platform
> - [copilot-instructions.md](https://github.com/home-assistant/core/blob/dev/.github/copilot-instructions.md)

## 代码风格

- **字符串小写**: 用户界面文本使用小写，除非是专有名词
  - 来源: PR #151479 - `"title": "Select DALI gateway"` 应使用小写 gateway
- **魔法字符串常量化**: 重复出现的字符串应定义为常量
  - 来源: PR #151479 - `gateway = DaliGateway(entry.data["gateway"])` 建议使用常量
- **移除空字段**: 删除字典和配置中未使用的空字段
  - 来源: PR #151479 - "please remove empty fields"
- **类型注解**: 移除不必要的类型覆盖，补充缺失的类型
  - 来源: PR #151479 - "Type overwrite not needed"

## 日志规范

- **日志级别选择**:
  - `debug`: 发现、状态变化、常规操作
  - `info`: 用户相关事件（设置完成等）
  - `warning`: 可恢复的问题
  - `error`: 不可恢复的故障
  - 来源: PR #151479 - "Let's log this on debug"
- **日志语句放在 try 块外**: 只在 try 中包裹可能抛异常的代码
  - 来源: PR #151479 - "Please keep the info logger out of the try block"
- **不需要 exception 日志**: 从异常重新抛出时会自动打印堆栈
  - 来源: PR #151479 - "I don't think an exception logger is needed as raising from an exception already prints the stacktrace"
- **日志不含集成名称**: HA 会自动添加
  - 来源: copilot-instructions.md

## 异常处理

- **缩小 try 块范围**: 只包裹真正可能抛异常的代码
  - 来源: PR #151479 - "only have things in the try block that can raise"
- **捕获具体异常**: 不使用裸 `except:`
  - 来源: copilot-instructions.md - "Bare exceptions are restricted to config flows and background tasks"
- **数据处理放 try 外**: 验证和处理逻辑应在 try 块之后
  - 来源: copilot-instructions.md - "Wrap only code that throws exceptions; process data afterward"

## 实体与设备

- **实体命名**: 主要功能实体设置 `_attr_name = None`（继承设备名）
  - 来源: PR #151479 - "If the entity is the main feature of the device, you can set the `_attr_name = None`"
- **Unique ID**: 使用设备序列号/MAC 地址，永不使用 IP 地址
  - 来源: copilot-instructions.md - "Use device serial numbers, MAC addresses, or config entry IDs—never IP addresses"
- **设备类型**: 使用合适的 device_class 提供上下文
  - 来源: copilot-instructions.md
- **Listener 注册模式**: 在 `async_added_to_hass` 中注册，用 `async_on_remove` 包装
  - 来源: PR #161415 - 确保实体移除时自动清理 listener

```python
async def async_added_to_hass(self) -> None:
    """Register listener."""
    await super().async_added_to_hass()
    self.async_on_remove(
        self._device.register_listener(
            CallbackEventType.XXX, self._handle_update
        )
    )
```

## Config Flow

- **UI 文本**: 避免 "Click"（用 "Select"），减少大写，只加粗按钮标签
  - 来源: PR #151479 - "We try to avoid 'Click' for touch devices like mobile"
- **100% 测试覆盖**: 所有路径（成功、错误、边缘情况）都要测试
  - 来源: PR #159270 - "Config flows require a 100% test coverage"

## 服务注册

- **在 async_setup() 中注册**: 不在 async_setup_entry() 中
  - 来源: copilot-instructions.md - "Services register in async_setup(), not async_setup_entry()"
- **验证 entry 状态**: 执行前检查 entry 存在且已加载
  - 来源: copilot-instructions.md - "Always validate config entry existence and loaded state"
- **抛出 ServiceValidationError**: 用于输入验证失败
  - 来源: copilot-instructions.md

## 文档规范

- **简洁的文档字符串**: 解释"为什么"，而非仅仅"是什么"
  - 来源: copilot-instructions.md - "Use concise docstrings explaining the 'why' behind code"
- **日志不含敏感信息**: 密码、token 等
  - 来源: copilot-instructions.md

## 外部依赖

- **必须在 PyPI 上托管**: 所有外部通信代码必须封装在独立的 Python 库中
  - 来源: [Development Checklist](https://developers.home-assistant.io/docs/development_checklist/) - "All communication to external devices or services must be wrapped in an external Python library hosted on pypi"
- **版本固定**: manifest.json 中的依赖必须指定精确版本（如 `phue==0.8.1`）
  - 来源: [Code Review](https://developers.home-assistant.io/docs/creating_component_code_review/)
- **公开仓库 + CI**: 库必须有公开 Git 仓库和自动化 CI
  - 来源: PR #159270 review comments
- **Issue 追踪器**: 库必须启用 issue 追踪
  - 来源: Development Checklist

## manifest.json

- **必填字段**: domain, name, codeowners, documentation, iot_class, requirements
  - 来源: [Integration Manifest](https://developers.home-assistant.io/docs/creating_integration_manifest/)
- **IoT Class 正确选择**:
  - `local_polling`: 本地轮询
  - `local_push`: 本地推送
  - `cloud_polling`: 云端轮询
  - `cloud_push`: 云端推送
  - 来源: copilot-instructions.md
- **quality_scale.yaml**: 新集成必须包含此文件
  - 来源: PR #159270 - "You are currently missing the quality_scale file"

## 开发环境

- **pre-commit hooks**: 必须配置开发环境，hassfest 会生成必需文件
  - 来源: PR #159270 - "please make sure to use a proper dev environment (dev container, etc.)"
- **requirements_all.txt**: 新依赖需运行 `python3 -m script.gen_requirements_all`
  - 来源: Development Checklist
- **CODEOWNERS**: 新代码所有者需运行 `python3 -m script.hassfest`
  - 来源: Development Checklist

## Coordinator 模式

- **使用 DataUpdateCoordinator**: 统一管理数据更新和错误处理
  - 来源: copilot-instructions.md
- **合理的更新间隔**: 避免过于频繁的轮询
  - 来源: copilot-instructions.md
- **设备自动发现**: 初始设置后应自动检测新设备
  - 来源: copilot-instructions.md - "Integrations should auto-detect new devices after initial setup"

## 设备管理

- **动态设备添加**: 使用 listener callbacks
  - 来源: copilot-instructions.md
- **过期设备清理**: 更新 device registry 移除不再存在的设备
  - 来源: PR #156015 - "Enhance Sunricher DALI with stale-device cleanup"
- **设备信息完整**: manufacturer, model, sw_version 等
  - 来源: copilot-instructions.md

## Diagnostics

- **敏感数据脱敏**: 使用 `async_redact_data()` 处理密码、token、IP 等
  - 来源: copilot-instructions.md - "Diagnostics must redact sensitive data"
- **包含有用的调试信息**: 设备状态、配置、连接信息
  - 来源: Quality Scale Gold tier

## Repair Issues

- **可操作的步骤**: 翻译字符串必须包含问题说明、重要性、编号的解决步骤
  - 来源: copilot-instructions.md - "Repair issues require actionable user steps in translated strings"

## PR 规范

- **最小化范围**: 一个 PR 只做一件事（一个功能、一个 bug 修复、一次重构）
  - 来源: [Review Process](https://developers.home-assistant.io/docs/review-process/) - "Make your PRs as small as possible"
- **签署 CLA**: 必须签署 Contributor License Agreement
  - 来源: PR review bot
- **遵守 ADR**: 检查 ADR 文件夹中的架构决策
  - 来源: Review Process - "Comply with architectural decisions documented in the ADR folder"

## Snapshot Testing

**强烈建议**：所有 platform 测试都应使用 snapshot testing。这是 HA Core 的最佳实践。

### 为什么必须使用 Snapshot

- 自动验证实体注册信息（unique_id、device_class、translation_key 等）
- 捕获意外的属性变化
- 提供可审查的实体状态快照
- 减少手动断言代码

### 必须添加 Snapshot 的场景

| 场景 | 说明 |
|------|------|
| 新增 platform | 每个 `test_{platform}.py` 必须有 `test_setup_entry` 使用 snapshot |
| 新增实体类型 | 验证 EntityRegistryEntry 和 State 完整 |
| 修改实体属性 | 运行 `--snapshot-update` 后审查 diff |

### 基本模式

```python
from tests.common import SnapshotAssertion, snapshot_platform

async def test_setup_entry(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test entity setup with snapshot verification."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
```

- 来源: ha-core 测试实践

### 禁止使用 TestClass

HA Core 不使用测试类，应使用模块级 fixture override：

```python
# ❌ 错误 - 不要使用 TestClass
class TestEnergySensor:
    @pytest.fixture
    def mock_devices(self, ...): ...

# ✅ 正确 - 使用模块级 fixture override
@pytest.fixture
def mock_devices(mock_light_device: MagicMock) -> list[MagicMock]:
    """Override fixture for this test module."""
    return [mock_light_device]
```

- 来源: PR #161415 - "We don't have test classes like this"

### 合并 Snapshot 测试

每个 platform 只需一个 `test_setup_entry` snapshot 测试，不要为不同实体类型创建多个：

- 来源: PR #161415 - "Can we merge this with the other snapshot test?"

### 更新 Snapshot

```bash
pytest tests/components/{domain}/test_{platform}.py --snapshot-update
```

### Snapshot 验证内容

- EntityRegistryEntrySnapshot: unique_id, device_class, entity_category, translation_key 等
- StateSnapshot: state, attributes
