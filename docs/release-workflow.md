# Plugin Release Workflow / 插件发布工作流

This document describes the workflow for releasing plugin updates.

本文档描述了发布插件更新的工作流程。

---

## Overview / 概述

The release workflow consists of the following components:

发布工作流包含以下组件：

1. **CHANGELOG.md** - Records all notable changes / 记录所有重要更改
2. **Version Extraction Script** - Automatically extracts plugin versions / 自动提取插件版本
3. **GitHub Actions Workflows** - Automates the release process / 自动化发布流程

---

## Release Process / 发布流程

### Step 1: Update Plugin Version / 更新插件版本

When you make changes to a plugin, update the version number in the plugin's docstring:

当您对插件进行更改时，更新插件文档字符串中的版本号：

```python
"""
title: My Plugin
author: Fu-Jie
version: 0.2.0  # <- Update this / 更新这里
...
"""
```

### Step 2: Update CHANGELOG / 更新更新日志

Add your changes to the `[Unreleased]` section in `CHANGELOG.md`:

在 `CHANGELOG.md` 的 `[Unreleased]` 部分添加您的更改：

```markdown
## [Unreleased] / 未发布

### Added / 新增
- New feature in Smart Mind Map / 智能思维导图新功能

### Changed / 变更
- Improved performance / 性能优化

### Fixed / 修复
- Fixed bug in export / 修复导出 bug
```

### Step 3: Create a Release / 创建发布

#### Option A: Manual Release (Recommended) / 手动发布（推荐）

1. Go to GitHub Actions → "Plugin Release / 插件发布"
2. Click "Run workflow"
3. Fill in the details:
   - **version**: e.g., `v1.0.0`
   - **release_title**: e.g., "Smart Mind Map Major Update"
   - **release_notes**: Additional notes in Markdown
   - **prerelease**: Check if this is a pre-release

1. 前往 GitHub Actions → "Plugin Release / 插件发布"
2. 点击 "Run workflow"
3. 填写详细信息：
   - **version**: 例如 `v1.0.0`
   - **release_title**: 例如 "智能思维导图重大更新"
   - **release_notes**: Markdown 格式的附加说明
   - **prerelease**: 如果是预发布版本则勾选

#### Option B: Tag-based Release / 基于标签的发布

```bash
# Create and push a version tag / 创建并推送版本标签
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

This will automatically trigger the release workflow.

这将自动触发发布工作流。

### Step 4: Finalize CHANGELOG / 完成更新日志

After the release, move the `[Unreleased]` content to a new version section:

发布后，将 `[Unreleased]` 的内容移动到新的版本部分：

```markdown
## [Unreleased] / 未发布
<!-- Empty for now / 暂时为空 -->

## [1.0.0] - 2024-01-15

### Added / 新增
- New feature in Smart Mind Map

### Plugin Updates / 插件更新
- `Smart Mind Map`: v0.7.0 → v0.8.0
```

---

## Version Numbering / 版本编号

We follow [Semantic Versioning](https://semver.org/):

我们遵循[语义化版本](https://semver.org/lang/zh-CN/)：

- **MAJOR (主版本)**: Breaking changes / 不兼容的变更
- **MINOR (次版本)**: New features, backwards compatible / 新功能，向后兼容
- **PATCH (补丁版本)**: Bug fixes / Bug 修复

### Examples / 示例

| Change Type / 变更类型 | Version Change / 版本变化 |
|----------------------|--------------------------|
| Bug fix / Bug 修复 | 0.1.0 → 0.1.1 |
| New feature / 新功能 | 0.1.1 → 0.2.0 |
| Breaking change / 不兼容变更 | 0.2.0 → 1.0.0 |

---

## GitHub Actions Workflows / GitHub Actions 工作流

### release.yml

**Trigger / 触发条件:**
- Manual workflow dispatch / 手动触发
- Push of version tags (`v*`) / 推送版本标签

**Actions / 动作:**
1. Extracts all plugin versions / 提取所有插件版本
2. Generates release notes / 生成发布说明
3. Creates GitHub Release / 创建 GitHub Release

### plugin-version-check.yml

**Trigger / 触发条件:**
- Pull requests that modify `plugins/**/*.py` / 修改 `plugins/**/*.py` 的 PR

**Actions / 动作:**
1. Compares plugin versions between base and PR / 比较基础分支和 PR 的插件版本
2. Comments on PR with version changes / 在 PR 上评论版本变化

---

## Scripts / 脚本

### extract_plugin_versions.py

Usage / 用法:

```bash
# Output to console / 输出到控制台
python scripts/extract_plugin_versions.py

# Output as JSON / 输出为 JSON
python scripts/extract_plugin_versions.py --json

# Output as Markdown table / 输出为 Markdown 表格
python scripts/extract_plugin_versions.py --markdown

# Compare with previous version / 与之前版本比较
python scripts/extract_plugin_versions.py --compare old_versions.json

# Save to file / 保存到文件
python scripts/extract_plugin_versions.py --json --output versions.json
```

---

## Best Practices / 最佳实践

1. **Always update version numbers** when making functional changes to plugins
   - 对插件进行功能性更改时**始终更新版本号**

2. **Write clear changelog entries** describing what changed and why
   - 编写清晰的更新日志条目，描述更改内容和原因

3. **Test locally** before creating a release
   - 在创建发布之前**本地测试**

4. **Use pre-releases** for testing new features
   - 使用**预发布**测试新功能

5. **Reference issues** in changelog entries when applicable
   - 在适用时在更新日志条目中**引用 issue**

---

## Author

Fu-Jie  
GitHub: [Fu-Jie/awesome-openwebui](https://github.com/Fu-Jie/awesome-openwebui)
