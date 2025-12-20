# 贡献指南 (Contributing Guide)

感谢你对 **OpenWebUI Extras** 感兴趣！我们非常欢迎社区贡献更多的插件、提示词和创意。

## 🤝 如何贡献

### 1. 分享提示词 (Prompts)

如果你有一个好用的提示词：
1. 在 `prompts/` 目录下找到合适的分类（如 `coding/`, `writing/`）。如果没有合适的，可以新建一个文件夹。
2. 创建一个新的 `.md` 或 `.json` 文件。
3. 提交 Pull Request (PR)。

### 2. 开发插件 (Plugins)

如果你开发了一个新的 OpenWebUI 插件 (Function/Tool)：
1. 确保你的插件代码包含完整的元数据（Frontmatter）：
   ```python
   """
   title: 插件名称
   author: 你的名字
   version: 0.1.0
   description: 简短描述插件的功能
   """
   ```
2. 将插件文件放入 `plugins/` 目录下的合适位置：
   - `plugins/actions/`: 用于添加按钮或修改消息的 Action 插件。
   - `plugins/filters/`: 用于拦截请求或响应的 Filter 插件。
   - `plugins/pipes/`: 用于自定义模型或 API 的 Pipe 插件。
   - `plugins/tools/`: 用于 LLM 调用的 Tool 插件。
3. 建议在 `docs/` 下添加一个简单的使用说明。

### 3. 改进文档

如果你发现文档有错误或可以改进的地方，直接提交 PR 即可。

## 🛠️ 开发规范

- **代码风格**：Python 代码请遵循 PEP 8 规范。
- **注释**：关键逻辑请添加注释，方便他人理解。
- **测试**：提交前请在本地 OpenWebUI 环境中测试通过。

## 📝 提交 PR

1. Fork 本仓库。
2. 创建一个新的分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 开启一个 Pull Request。

再次感谢你的贡献！🚀
