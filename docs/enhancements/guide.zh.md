# OpenWebUI 增强指南

一份全面的指南，帮助你优化与自定义 OpenWebUI 的使用体验。

---

## 性能优化

### 上下文管理

合理管理上下文可显著提升回复质量并降低成本。

!!! tip "使用上下文压缩"
    安装 [Async Context Compression](../plugins/filters/async-context-compression.md) 过滤器，自动管理长对话。

#### 最佳实践

1. **清理旧对话**：归档或删除旧聊天保持界面整洁
2. **聚焦会话**：新话题开启新会话
3. **利用系统提示词**：明确边界与关注点
4. **监控 Token**：关注上下文长度

### 模型选择

根据任务选择合适的模型：

| 任务类型 | 推荐方式 |
|-----------|---------------------|
| 快速提问 | 较小、较快的模型 |
| 复杂分析 | 更强大的模型 |
| 创意写作 | 提高温度的模型 |
| 代码生成 | 面向代码的模型 |

---

## 自定义技巧

### 键盘快捷键

常用快捷键可以加速工作流：

| 快捷键 | 动作 |
|----------|--------|
| `Enter` | 发送消息 |
| `Shift + Enter` | 换行 |
| `↑` | 编辑上一条消息 |
| `Ctrl + /` | 切换侧边栏 |

### 界面自定义

1. **深浅色模式**：使用顶部导航的主题切换
2. **侧边栏整理**：固定常用对话
3. **模型收藏**：标星高频模型

### 系统提示词模板

为常见场景创建可复用的系统提示词：

```text
# Template: Technical Assistant
You are a technical assistant specializing in [DOMAIN].
Focus on providing accurate, actionable information.
When unsure, acknowledge limitations and suggest resources.
```

---

## 工作流优化

### 面向开发者

1. **代码审查流水线**
   - 使用编程类提示词进行初审
   - 通过过滤器保持格式一致
   - 导出到 Excel 便于跟踪

2. **文档生成**
   - 从 Document Formatter 提示词开始
   - 使用 Summary Action 提炼要点
   - 输出结构化内容

### 面向内容创作者

1. **内容生产**
   - 使用 Marketing 提示词进行创意发散
   - 迭代反馈完善
   - 导出最终版本

2. **研究工作流**
   - 采用多模型获取多元观点
   - 利用思维导图可视化
   - 创建知识卡片记录要点

### 面向学习者

1. **学习会话**
   - 技术主题用 Code Explainer 讲解
   - 生成知识卡片用于记忆
   - 复杂主题用思维导图梳理

---

## 插件组合

### 推荐组合

=== "Developer Stack"
    - **Filter**: Context Enhancement
    - **Action**: Export to Excel
    - **Prompt**: Senior Developer Assistant

=== "Researcher Stack"
    - **Filter**: Async Context Compression
    - **Action**: Smart Mind Map
    - **Pipeline**: MoE Prompt Refiner

=== "Student Stack"
    - **Action**: Knowledge Card
    - **Action**: Smart Mind Map
    - **Prompt**: Code Explainer

---

## 高级配置

### 自定义 Valves

很多插件支持 Valves（配置项）。在以下位置可配置：

1. **Admin Panel** → **Settings** → **Functions**
2. 点开目标插件
3. 修改 Valve 设置
4. 保存变更

### 用户级覆盖

部分插件支持 UserValves，允许用户覆盖全局配置：

```python
class UserValves(BaseModel):
    custom_setting: str = Field(
        default="",
        description="User-specific configuration"
    )
```

---

## 故障排查

### 常见问题

??? question "插件更新后无法工作？"
    尝试禁用再启用插件，或重新上传最新版。

??? question "回复太慢？"
    - 检查网络连接
    - 尝试更小的模型
    - 若未开启流式输出，可尝试启用

??? question "上下文丢失？"
    - 查看上下文压缩是否过度
    - 调整 `preserve_recent` 设置
    - 需要时开启新对话

### 获取帮助

- 查阅插件文档
- 查看 OpenWebUI 官方文档
- 加入社区讨论

---

## 资源

- [:fontawesome-brands-github: OpenWebUI GitHub](https://github.com/open-webui/open-webui)
- [:material-book-open-variant: 官方文档](https://docs.openwebui.com/)
- [:material-forum: 社区讨论](https://github.com/open-webui/open-webui/discussions)
