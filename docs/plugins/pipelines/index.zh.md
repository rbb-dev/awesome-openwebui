# Pipeline 插件

Pipeline 是组合多步处理的复杂工作流，适用于高级场景。

## 什么是 Pipelines？

Pipelines 不仅是简单转换，还可以实现：

- :material-workflow: 多步骤处理流程
- :material-source-merge: 模型编排
- :material-robot-industrial: 高级智能体行为
- :material-cog-box: 复杂业务逻辑

---

## 可用的 Pipeline 插件

<div class="grid cards" markdown>

-   :material-view-module:{ .lg .middle } **MoE Prompt Refiner**

    ---

    为 Mixture of Experts（MoE）汇总请求优化提示词，生成高质量综合报告。

    **版本：** 1.0.0

    [:octicons-arrow-right-24: 查看文档](moe-prompt-refiner.md)

</div>

---

## Pipelines 的区别

| 特性 | Filters | Pipes | Pipelines |
|---------|---------|-------|-----------|
| 复杂度 | 低 | 中 | 高 |
| 主要用途 | 消息处理 | 模型集成 | 多步工作流 |
| 执行方式 | LLM 前后 | 作为 LLM | 自定义编排 |
| 依赖 | 极少 | API 访问 | 往往多个服务 |

---

## 快速安装

1. 下载 Pipeline `.py` 文件
2. 前往 **Admin Panel** → **Settings** → **Functions**
3. 上传并配置所需服务
4. 启用该 Pipeline

---

## 开发注意事项

Pipeline 通常需要：

- 多个 API 集成
- 跨步骤的状态管理
- 每一步的错误处理
- 性能优化

详见 [插件开发指南](../../development/plugin-guide.md)。
