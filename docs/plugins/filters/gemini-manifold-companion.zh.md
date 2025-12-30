# Gemini Manifold Companion

<span class="category-badge filter">Filter</span>
<span class="version-badge">v1.0.0</span>

Gemini Manifold Pipe 的伴随过滤器，用于增强 Gemini 集成的处理效果。

---

## 概览

Gemini Manifold Companion 与 [Gemini Manifold Pipe](../pipes/gemini-manifold.md) 搭配使用，为 Gemini 模型集成提供额外的处理与优化。

## 功能特性

- :material-handshake: **无缝协同**：与 Gemini Manifold Pipe 配合工作
- :material-format-text: **消息格式化**：针对 Gemini 优化消息
- :material-shield: **错误处理**：更友好的 API 异常处理
- :material-tune: **精细配置**：提供额外调优选项

---

## 安装

1. 先安装 [Gemini Manifold Pipe](../pipes/gemini-manifold.md)
2. 下载伴随过滤器：[`gemini_manifold_companion.py`](https://github.com/Fu-Jie/awesome-openwebui/tree/main/plugins/filters/gemini_manifold_companion)
3. 上传到 OpenWebUI：**Admin Panel** → **Settings** → **Functions**
4. 启用过滤器

---

## 配置项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `auto_format` | boolean | `true` | 为 Gemini 自动格式化消息 |
| `handle_errors` | boolean | `true` | 开启错误处理 |

---

## 运行要求

!!! warning "依赖"
    本过滤器需要先安装并配置 **Gemini Manifold Pipe**。

!!! note "前置条件"
    - OpenWebUI v0.3.0 及以上
    - 已安装 Gemini Manifold Pipe

---

## 源码

[:fontawesome-brands-github: 在 GitHub 查看](https://github.com/Fu-Jie/awesome-openwebui/tree/main/plugins/filters/gemini_manifold_companion){ .md-button }
