# 插件发布工作流

本文档描述了发布插件更新的工作流程。

---

## 概述

发布工作流包含以下组件：

1. **CHANGELOG.md** - 记录所有重要更改
2. **版本提取脚本** - 自动提取插件版本信息
3. **GitHub Actions 工作流** - 自动化发布流程

---

## 发布流程

### 第 1 步：更新插件版本

当您对插件进行更改时，更新插件文档字符串中的版本号：

```python
"""
title: 我的插件
author: Fu-Jie
version: 0.2.0  # <- 更新这里
...
"""
```

### 第 2 步：更新更新日志

在 `CHANGELOG.md` 的 `[Unreleased]` 部分添加您的更改：

```markdown
## [Unreleased] / 未发布

### Added / 新增
- 智能思维导图新功能

### Changed / 变更
- 性能优化

### Fixed / 修复
- 修复导出 bug
```

### 第 3 步：创建发布

#### 方式 A：手动发布（推荐）

1. 前往 GitHub Actions → "Plugin Release / 插件发布"
2. 点击 "Run workflow"
3. 填写详细信息：
   - **version**: 例如 `v1.0.0`
   - **release_title**: 例如 "智能思维导图重大更新"
   - **release_notes**: Markdown 格式的附加说明
   - **prerelease**: 如果是预发布版本则勾选

#### 方式 B：基于标签的发布

```bash
# 创建并推送版本标签
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

这将自动触发发布工作流。

### 第 4 步：完成更新日志

发布后，将 `[Unreleased]` 的内容移动到新的版本部分：

```markdown
## [Unreleased] / 未发布
<!-- 暂时为空 -->

## [1.0.0] - 2024-01-15

### Added / 新增
- 智能思维导图新功能

### Plugin Updates / 插件更新
- `Smart Mind Map / 思维导图`: v0.7.0 → v0.8.0
```

---

## 版本编号

我们遵循[语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本 (MAJOR)**: 不兼容的 API 变更
- **次版本 (MINOR)**: 向后兼容的新功能
- **补丁版本 (PATCH)**: 向后兼容的 Bug 修复

### 示例

| 变更类型 | 版本变化 |
|---------|---------|
| Bug 修复 | 0.1.0 → 0.1.1 |
| 新功能 | 0.1.1 → 0.2.0 |
| 不兼容变更 | 0.2.0 → 1.0.0 |

---

## GitHub Actions 工作流

### release.yml

**触发条件:**
- 手动触发 (workflow_dispatch)
- 推送版本标签 (`v*`)

**动作:**
1. 提取所有插件版本
2. 生成发布说明
3. 创建 GitHub Release

### plugin-version-check.yml

**触发条件:**
- 修改 `plugins/**/*.py` 的 Pull Request

**动作:**
1. 比较基础分支和 PR 的插件版本
2. 在 PR 上评论版本变化

---

## 脚本使用

### extract_plugin_versions.py

```bash
# 输出到控制台
python scripts/extract_plugin_versions.py

# 输出为 JSON
python scripts/extract_plugin_versions.py --json

# 输出为 Markdown 表格
python scripts/extract_plugin_versions.py --markdown

# 与之前版本比较
python scripts/extract_plugin_versions.py --compare old_versions.json

# 保存到文件
python scripts/extract_plugin_versions.py --json --output versions.json
```

---

## 最佳实践

1. **始终更新版本号** - 对插件进行功能性更改时
2. **编写清晰的更新日志** - 描述更改内容和原因
3. **本地测试** - 在创建发布之前
4. **使用预发布** - 测试新功能
5. **引用 issue** - 在适用时在更新日志条目中

---

## 作者

Fu-Jie  
GitHub: [Fu-Jie/awesome-openwebui](https://github.com/Fu-Jie/awesome-openwebui)
