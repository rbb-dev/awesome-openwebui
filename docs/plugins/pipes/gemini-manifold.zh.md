# Gemini Manifold

<span class="category-badge pipe">Pipe</span>
<span class="version-badge">v1.0.0</span>

面向 Google Gemini 模型的集成流水线，支持完整流式返回。

---

## 概览

Gemini Manifold Pipe 提供与 Google Gemini AI 模型的无缝集成。它会将 Gemini 模型作为可选项暴露在 OpenWebUI 中，你可以像使用其他模型一样使用它们。

## 功能特性

- :material-google: **完整 Gemini 支持**：可使用所有 Gemini 模型变体
- :material-stream: **流式输出**：实时流式响应
- :material-image: **多模态**：支持图像与文本
- :material-shield: **错误处理**：健壮的错误管理
- :material-tune: **可配置**：可自定义模型参数

---

## 安装

1. 下载插件文件：[`gemini_manifold.py`](https://github.com/Fu-Jie/awesome-openwebui/tree/main/plugins/pipes/gemini_mainfold)
2. 上传到 OpenWebUI：**Admin Panel** → **Settings** → **Functions**
3. 配置你的 Gemini API Key
4. 在模型下拉中选择 Gemini 模型

---

## 配置

| 选项 | 类型 | 是否必填 | 说明 |
|--------|------|----------|-------------|
| `GEMINI_API_KEY` | string | 是 | 你的 Google AI Studio API Key |
| `DEFAULT_MODEL` | string | 否 | 默认使用的 Gemini 模型 |
| `TEMPERATURE` | float | 否 | 输出温度（0-1） |
| `MAX_TOKENS` | integer | 否 | 最大回复 token 数 |

---

## 可用模型

配置完成后，你可以选择以下模型：

- `gemini-pro` —— 纯文本模型
- `gemini-pro-vision` —— 多模态模型
- `gemini-1.5-pro` —— 最新 Pro 模型
- `gemini-1.5-flash` —— 快速响应模型

---

## 使用方法

1. 安装后进入任意对话
2. 打开模型选择下拉
3. 查找以 Pipe 名称前缀的模型
4. 选择 Gemini 模型
5. 开始聊天！

---

## 获取 API Key

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 创建新的 API Key
3. 复制并粘贴到插件配置中

!!! warning "API Key 安全"
    请妥善保管你的 API Key，不要公开或提交到版本库。

---

## 伴随过滤器

如需增强功能，可安装 [Gemini Manifold Companion](../filters/gemini-manifold-companion.md) 过滤器。

---

## 运行要求

!!! note "前置条件"
    - OpenWebUI v0.3.0 及以上
    - 有效的 Gemini API Key
    - 可访问 Google AI API 的网络

---

## 常见问题

??? question "模型没有出现？"
    请确认 API Key 配置正确且插件已启用。

??? question "出现 API 错误？"
    检查 Google AI Studio 中的 Key 有效性和额度限制。

??? question "响应较慢？"
    可尝试使用 `gemini-1.5-flash` 获得更快速度。

---

## 源码

[:fontawesome-brands-github: 在 GitHub 查看](https://github.com/Fu-Jie/awesome-openwebui/tree/main/plugins/pipes/gemini_mainfold){ .md-button }
