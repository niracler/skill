# Push Review Mode

使用 git push 选项创建合并请求的零安装方案。

## 可用选项

### 创建新 MR

```bash
git push -o review=new
```

即使该分支已有 MR，也会创建新的合并请求。

### 更新已有 MR

```bash
git push -o review=<MR-ID>
```

通过 ID 更新指定的合并请求。当同一目标分支有多个 MR 时很有用。

### 强制更新

```bash
git push -o review=<MR-ID> -o old-oid=<commit-hash>
```

用本地版本强制覆盖。谨慎使用——可能会丢弃他人的更改。

### 跳过评审

```bash
git push -o review=no
```

绕过评审直接推送。需要分支的推送权限。

## 常见工作流

### 功能分支到主分支

```bash
# 创建功能分支
git checkout -b feature/my-feature

# 修改并提交
git add .
git commit -m "feat: add new feature"

# 推送并创建 MR
git push -u origin feature/my-feature -o review=new
```

### 快速修复无需评审

```bash
# 用于修复错字或小问题（如果有权限）
git push -o review=no
```

## 与 git pr 对比

| 功能 | Push Review Mode | git pr |
|------|------------------|--------|
| 需要安装 | 否 | 是 |
| 编辑器填写标题/描述 | 否 | 是 |
| 指定评审人 | 否 | 是 |
| 草稿模式 | 否 | 是 |
| 离线工作 | N/A | N/A |

**建议:** 快速创建 MR 用 Push Review Mode。需要指定评审人或草稿模式时用 git pr。

## 参考链接

- [Push Review Mode 文档](https://help.aliyun.com/zh/yunxiao/user-guide/push-review-mode)
