# Summary（摘要）

<span class="category-badge action">Action</span>
<span class="version-badge">v1.0.0</span>

为长文本生成简洁摘要，并提取关键要点。

---

## 概览

Summary 插件可以快速理解长文本，生成精炼摘要并列出关键点，适合：

- 总结长文章或文档
- 从对话中提炼要点
- 为复杂主题制作快速概览

## 功能特性

- :material-text-box-search: **智能摘要**：AI 驱动的内容分析
- :material-format-list-bulleted: **关键点**：提取重要信息
- :material-content-copy: **便捷复制**：一键复制摘要
- :material-tune: **长度可调**：可选择摘要详略程度

---

## 安装

1. 下载插件文件：[`summary.py`](https://github.com/Fu-Jie/awesome-openwebui/tree/main/plugins/actions/summary)
2. 上传到 OpenWebUI：**Admin Panel** → **Settings** → **Functions**
3. 启用插件

---

## 使用方法

1. 获取一段较长的 AI 回复或粘贴长文本
2. 点击消息操作栏的 **Summary** 按钮
3. 查看生成的摘要与关键点

---

## 配置项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `summary_length` | string | `"medium"` | 摘要长度（short/medium/long） |
| `include_key_points` | boolean | `true` | 是否提取并列出关键点 |
| `language` | string | `"auto"` | 输出语言 |

---

## 输出示例

```markdown
## Summary

This document discusses the implementation of a new feature 
for the application, focusing on user experience improvements 
and performance optimizations.

### Key Points

- ✅ New user interface design improves accessibility
- ✅ Backend optimizations reduce load times by 40%
- ✅ Mobile responsiveness enhanced
- ✅ Integration with third-party services simplified
```

---

## 运行要求

!!! note "前置条件"
    - OpenWebUI v0.3.0 及以上
    - 使用当前会话的 LLM 模型进行摘要

---

## 源码

[:fontawesome-brands-github: 在 GitHub 查看](https://github.com/Fu-Jie/awesome-openwebui/tree/main/plugins/actions/summary){ .md-button }
