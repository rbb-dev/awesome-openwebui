"""
title: Context & Model Enhancement Filter
author: Fu-Jie
author_url: https://github.com/Fu-Jie
funding_url: https://github.com/Fu-Jie/awesome-openwebui
version: 0.2

description:
    一个功能全面的 Filter 插件，用于增强请求上下文和优化模型功能。提供四大核心功能：

    1. 环境变量注入：在每条用户消息前自动注入用户环境变量（用户名、时间、时区、语言等）
       - 支持纯文本、图片、多模态消息
       - 幂等性设计，避免重复注入
       - 注入成功时发送前端状态提示

    2. Web Search 功能改进：为特定模型优化 Web 搜索功能
       - 为阿里云通义千问系列、DeepSeek、Gemini 等模型添加搜索能力
       - 自动识别模型并追加 "-search" 后缀
       - 管理功能开关，防止冲突
       - 启用时发送搜索能力状态提示

    3. 模型适配与上下文注入：为特定模型注入 chat_id 等上下文信息
       - 支持 cfchatqwen、webgemini 等模型的特殊处理
       - 动态模型重定向
       - 智能化的模型识别和适配

    4. 智能内容规范化：生产级的内容清洗与修复系统
       - 智能修复损坏的代码块（前缀、后缀、缩进）
       - 规范化 LaTeX 公式格式（行内/块级）
       - 优化思维链标签（</thought>）格式
       - 自动闭合未结束的代码块
       - 智能列表格式修复
       - 清理冗余的 XML 标签
       - 可配置的规则系统

features:
    - 自动化环境变量管理
    - 智能模型功能适配
    - 异步状态反馈
    - 幂等性保证
    - 多模型支持
    - 智能内容清洗与规范化
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Callable
import re
import logging
from dataclasses import dataclass, field


# 配置日志
logger = logging.getLogger(__name__)

@dataclass
class NormalizerConfig:
    """规范化配置类,用于动态启用/禁用特定规则"""
    enable_escape_fix: bool = True          # 修复转义字符
    enable_thought_tag_fix: bool = True     # 修复思考链标签
    enable_code_block_fix: bool = True      # 修复代码块格式
    enable_latex_fix: bool = True           # 修复 LaTeX 公式格式
    enable_list_fix: bool = False            # 修复列表换行
    enable_unclosed_block_fix: bool = True  # 修复未闭合代码块
    enable_fullwidth_symbol_fix: bool = False # 修复代码内的全角符号
    enable_xml_tag_cleanup: bool = True     # 清理 XML 残留标签
    
    # 自定义清理函数列表（高级扩展用）
    custom_cleaners: List[Callable[[str], str]] = field(default_factory=list)

class ContentNormalizer:
    """LLM 输出内容规范化器 - 生产级实现"""
    
    # --- 1. 预编译正则表达式（性能优化） ---
    _PATTERNS = {
        # 代码块前缀：如果 ``` 前面不是行首也不是换行符
        'code_block_prefix': re.compile(r'(?<!^)(?<!\n)(```)', re.MULTILINE),
        
        # 代码块后缀：匹配 ```语言名 后面紧跟非空白字符(没有换行)
        # 匹配 ```python code 这种情况，但不匹配 ```python 或 ```python\n
        'code_block_suffix': re.compile(r'(```[\w\+\-\.]*)[ \t]+([^\n\r])'),
        
        # 代码块缩进：行首的空白字符 + ```
        'code_block_indent': re.compile(r'^[ \t]+(```)', re.MULTILINE),
        
        # 思考链标签：</thought> 后可能跟空格或换行
        'thought_tag': re.compile(r'</thought>[ \t]*\n*'),
        
        # LaTeX 块级公式：\[ ... \]
        'latex_bracket_block': re.compile(r'\\\[(.+?)\\\]', re.DOTALL),
        # LaTeX 行内公式：\( ... \)
        'latex_paren_inline': re.compile(r'\\\((.+?)\\\)'),
        
        # 列表项：非换行符 + 数字 + 点 + 空格 (e.g. "Text1. Item")
        'list_item': re.compile(r'([^\n])(\d+\. )'),
        
        # XML 残留标签 (如 Claude 的 artifacts)
        'xml_artifacts': re.compile(r'</?(?:antArtifact|antThinking|artifact)[^>]*>', re.IGNORECASE),
    }
    
    def __init__(self, config: Optional[NormalizerConfig] = None):
        self.config = config or NormalizerConfig()
        self.applied_fixes = []
    
    def normalize(self, content: str) -> str:
        """主入口：按顺序应用所有规范化规则"""
        self.applied_fixes = []
        if not content:
            return content
        
        try:
            # 1. 转义字符修复（必须最先执行，否则影响后续正则）
            if self.config.enable_escape_fix:
                original = content
                content = self._fix_escape_characters(content)
                if content != original:
                    self.applied_fixes.append("修复转义字符")
            
            # 2. 思考链标签规范化
            if self.config.enable_thought_tag_fix:
                original = content
                content = self._fix_thought_tags(content)
                if content != original:
                    self.applied_fixes.append("规范化思考链")
            
            # 3. 代码块格式修复
            if self.config.enable_code_block_fix:
                original = content
                content = self._fix_code_blocks(content)
                if content != original:
                    self.applied_fixes.append("修复代码块格式")
            
            # 4. LaTeX 公式规范化
            if self.config.enable_latex_fix:
                original = content
                content = self._fix_latex_formulas(content)
                if content != original:
                    self.applied_fixes.append("规范化 LaTeX 公式")
            
            # 5. 列表格式修复
            if self.config.enable_list_fix:
                original = content
                content = self._fix_list_formatting(content)
                if content != original:
                    self.applied_fixes.append("修复列表格式")
            
            # 6. 未闭合代码块检测与修复
            if self.config.enable_unclosed_block_fix:
                original = content
                content = self._fix_unclosed_code_blocks(content)
                if content != original:
                    self.applied_fixes.append("闭合未结束代码块")
            
            # 7. 全角符号转半角（仅代码块内）
            if self.config.enable_fullwidth_symbol_fix:
                original = content
                content = self._fix_fullwidth_symbols_in_code(content)
                if content != original:
                    self.applied_fixes.append("全角符号转半角")
            
            # 8. XML 标签残留清理
            if self.config.enable_xml_tag_cleanup:
                original = content
                content = self._cleanup_xml_tags(content)
                if content != original:
                    self.applied_fixes.append("清理 XML 标签")
            
            # 9. 执行自定义清理函数
            for cleaner in self.config.custom_cleaners:
                original = content
                content = cleaner(content)
                if content != original:
                    self.applied_fixes.append("执行自定义清理")
            
            return content
            
        except Exception as e:
            # 生产环境保底机制：如果清洗过程报错，返回原始内容，避免阻断服务
            logger.error(f"内容规范化失败: {e}", exc_info=True)
            return content
    
    def _fix_escape_characters(self, content: str) -> str:
        """修复过度转义的字符"""
        # 注意：先处理具体的转义序列，再处理通用的双反斜杠
        content = content.replace("\\r\\n", "\n")
        content = content.replace("\\n", "\n")
        content = content.replace("\\t", "\t")
        # 修复过度转义的反斜杠 (例如路径 C:\\Users)
        content = content.replace("\\\\", "\\")
        return content
    
    def _fix_thought_tags(self, content: str) -> str:
        """规范化 </thought> 标签，统一为空两行"""
        return self._PATTERNS['thought_tag'].sub("</thought>\n\n", content)
    
    def _fix_code_blocks(self, content: str) -> str:
        """修复代码块格式（独占行、换行、去缩进）"""
        # C: 移除代码块前的缩进（必须先执行，否则影响下面的判断）
        content = self._PATTERNS['code_block_indent'].sub(r"\1", content)
        # A: 确保 ``` 前有换行
        content = self._PATTERNS['code_block_prefix'].sub(r"\n\1", content)
        # B: 确保 ```语言标识 后有换行
        content = self._PATTERNS['code_block_suffix'].sub(r"\1\n\2", content)
        return content
    
    def _fix_latex_formulas(self, content: str) -> str:
        """规范化 LaTeX 公式：\[ -> $$ (块级), \( -> $ (行内)"""
        content = self._PATTERNS['latex_bracket_block'].sub(r"$$\1$$", content)
        content = self._PATTERNS['latex_paren_inline'].sub(r"$\1$", content)
        return content
    
    def _fix_list_formatting(self, content: str) -> str:
        """修复列表项缺少换行的问题 (如 'text1. item' -> 'text\\n1. item')"""
        return self._PATTERNS['list_item'].sub(r"\1\n\2", content)
    
    def _fix_unclosed_code_blocks(self, content: str) -> str:
        """检测并修复未闭合的代码块"""
        if content.count("```") % 2 != 0:
            logger.warning("检测到未闭合的代码块，自动补全")
            content += "\n```"
        return content
    
    def _fix_fullwidth_symbols_in_code(self, content: str) -> str:
        """在代码块内将全角符号转为半角（精细化操作）"""
        # 常见误用的全角符号映射
        FULLWIDTH_MAP = {
            '，': ',', '。': '.', '（': '(', '）': ')',
            '【': '[', '】': ']', '；': ';', '：': ':',
            '？': '?', '！': '!', '"': '"', '"': '"',
            ''': "'", ''': "'",
        }
        
        parts = content.split("```")
        # 代码块内容位于索引 1, 3, 5... (奇数位)
        for i in range(1, len(parts), 2):
            for full, half in FULLWIDTH_MAP.items():
                parts[i] = parts[i].replace(full, half)
        
        return "```".join(parts)
    
    def _cleanup_xml_tags(self, content: str) -> str:
        """移除无关的 XML 标签"""
        return self._PATTERNS['xml_artifacts'].sub("", content)

class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def inlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __metadata__: Optional[dict] = None,
        __model__: Optional[dict] = None,
        __event_emitter__=None,
    ) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        messages = body.get("messages", [])
        self.insert_user_env_info(__metadata__, messages, __event_emitter__)
        # if "测试系统提示词" in str(messages):
        #     messages.insert(0, {"role": "system", "content": "你是一个大数学家"})
        #     print("XXXXX" * 100)
        #     print(body)
        self.change_web_search(body, __user__, __event_emitter__)
        body = self.inlet_chat_id(__model__, __metadata__, body)

        return body

    def inlet_chat_id(self, model: dict, metadata: dict, body: dict):
        if "openai" in model:
            base_model_id = model["openai"]["id"]

        else:
            base_model_id = model["info"]["base_model_id"]

        base_model = model["id"] if base_model_id is None else base_model_id
        if base_model.startswith("cfchatqwen"):
            # pass
            body["chat_id"] = metadata["chat_id"]

        if base_model.startswith("webgemini"):
            body["chat_id"] = metadata["chat_id"]
            if not model["id"].startswith("webgemini"):
                body["custom_model_id"] = model["id"]

        # print("我是 body *******************", body)
        return body

    def change_web_search(self, body, __user__, __event_emitter__=None):
        """
        优化特定模型的 Web 搜索功能。

        功能：
        - 检测是否启用了 Web 搜索
        - 为支持搜索的模型启用模型本身的搜索能力
        - 禁用默认的 web_search 开关以避免冲突
        - 当使用模型本身的搜索能力时发送状态提示

        参数：
            body: 请求体字典
            __user__: 用户信息
            __event_emitter__: 用于发送前端事件的发射器函数
        """
        features = body.get("features", {})
        web_search_enabled = (
            features.get("web_search", False) if isinstance(features, dict) else False
        )
        if isinstance(__user__, (list, tuple)):
            user_email = __user__[0].get("email", "用户") if __user__[0] else "用户"
        elif isinstance(__user__, dict):
            user_email = __user__.get("email", "用户")
        model_name = body.get("model")

        search_enabled_for_model = False
        if web_search_enabled:
            if model_name in ["qwen-max-latest", "qwen-max", "qwen-plus-latest"]:
                body.setdefault("enable_search", True)
                features["web_search"] = False
                search_enabled_for_model = True
            if "search" in model_name or "搜索" in model_name:
                features["web_search"] = False
            if model_name.startswith("cfdeepseek-deepseek") and not model_name.endswith(
                "search"
            ):
                body["model"] = body["model"] + "-search"
                features["web_search"] = False
                search_enabled_for_model = True
            if model_name.startswith("cfchatqwen") and not model_name.endswith(
                "search"
            ):
                body["model"] = body["model"] + "-search"
                features["web_search"] = False
                search_enabled_for_model = True
            if model_name.startswith("gemini-2.5") and "search" not in model_name:
                body["model"] = body["model"] + "-search"
                features["web_search"] = False
                search_enabled_for_model = True
            if user_email == "yi204o@qq.com":
                features["web_search"] = False

        # 如果启用了模型本身的搜索能力，发送状态提示
        if search_enabled_for_model and __event_emitter__:
            import asyncio

            try:
                asyncio.create_task(
                    self._emit_search_status(__event_emitter__, model_name)
                )
            except RuntimeError:
                pass

    def insert_user_env_info(
        self, __metadata__, messages, __event_emitter__=None, model_match_tags=None
    ):
        """
        在第一条用户消息中注入环境变量信息。

        功能特性：
        - 始终在用户消息内容前注入环境变量的 Markdown 说明
        - 支持多种消息类型：纯文本、图片、图文混合消息
        - 幂等性设计：若环境变量信息已存在则更新为最新数据，不会重复添加
        - 注入成功后通过事件发射器向前端发送"注入成功"的状态提示

        参数：
            __metadata__: 包含环境变量的元数据字典
            messages: 消息列表
            __event_emitter__: 用于发送前端事件的发射器函数
            model_match_tags: 模型匹配标签（保留参数，当前未使用）
        """
        variables = __metadata__.get("variables", {})
        if not messages or messages[0]["role"] != "user":
            return

        env_injected = False
        if variables:
            # 构建环境变量的Markdown文本
            variable_markdown = (
                "## 用户环境变量\n"
                "以下信息为用户的环境变量，可用于为用户提供更个性化的服务或满足特定需求时作为参考：\n"
                f"- **用户姓名**：{variables.get('{{USER_NAME}}', '')}\n"
                f"- **当前日期时间**：{variables.get('{{CURRENT_DATETIME}}', '')}\n"
                f"- **当前星期**：{variables.get('{{CURRENT_WEEKDAY}}', '')}\n"
                f"- **当前时区**：{variables.get('{{CURRENT_TIMEZONE}}', '')}\n"
                f"- **用户语言**：{variables.get('{{USER_LANGUAGE}}', '')}\n"
            )

            content = messages[0]["content"]
            # 环境变量部分的匹配模式
            env_var_pattern = r"(## 用户环境变量\n以下信息为用户的环境变量，可用于为用户提供更个性化的服务或满足特定需求时作为参考：\n.*?用户语言.*?\n)"
            # 处理不同内容类型
            if isinstance(content, list):  # 多模态内容(可能包含图片和文本)
                # 查找第一个文本类型的内容
                text_index = -1
                for i, part in enumerate(content):
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_index = i
                        break

                if text_index >= 0:
                    # 存在文本内容，检查是否已存在环境变量信息
                    text_part = content[text_index]
                    text_content = text_part.get("text", "")

                    if re.search(env_var_pattern, text_content, flags=re.DOTALL):
                        # 已存在环境变量信息，更新为最新数据
                        text_part["text"] = re.sub(
                            env_var_pattern,
                            variable_markdown,
                            text_content,
                            flags=re.DOTALL,
                        )
                    else:
                        # 不存在环境变量信息，添加到开头
                        text_part["text"] = f"{variable_markdown}\n{text_content}"

                    content[text_index] = text_part
                else:
                    # 没有文本内容(例如只有图片)，添加新的文本项
                    content.insert(
                        0, {"type": "text", "text": f"{variable_markdown}\n"}
                    )

                messages[0]["content"] = content

            elif isinstance(content, str):  # 纯文本内容
                # 检查是否已存在环境变量信息
                if re.search(env_var_pattern, content, flags=re.DOTALL):
                    # 已存在，更新为最新数据
                    messages[0]["content"] = re.sub(
                        env_var_pattern, variable_markdown, content, flags=re.DOTALL
                    )
                else:
                    # 不存在，添加到开头
                    messages[0]["content"] = f"{variable_markdown}\n{content}"
                env_injected = True

            else:  # 其他类型内容
                # 转换为字符串并处理
                str_content = str(content)
                # 检查是否已存在环境变量信息
                if re.search(env_var_pattern, str_content, flags=re.DOTALL):
                    # 已存在，更新为最新数据
                    messages[0]["content"] = re.sub(
                        env_var_pattern, variable_markdown, str_content, flags=re.DOTALL
                    )
                else:
                    # 不存在，添加到开头
                    messages[0]["content"] = f"{variable_markdown}\n{str_content}"
                env_injected = True

            # 环境变量注入成功后，发送状态提示给用户
            if env_injected and __event_emitter__:
                import asyncio

                try:
                    # 如果在异步环境中，使用 await
                    asyncio.create_task(self._emit_env_status(__event_emitter__))
                except RuntimeError:
                    # 如果不在异步环境中，直接调用
                    pass

    async def _emit_env_status(self, __event_emitter__):
        """
        发送环境变量注入成功的状态提示给前端用户
        """
        try:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "✓ 用户环境变量已注入成功",
                        "done": True,
                    },
                }
            )
        except Exception as e:
            print(f"发送状态提示时出错: {e}")

    async def _emit_search_status(self, __event_emitter__, model_name):
        """
        发送模型搜索功能启用的状态提示给前端用户
        """
        try:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"🔍 已为 {model_name} 启用搜索能力",
                        "done": True,
                    },
                }
            )
        except Exception as e:
            print(f"发送搜索状态提示时出错: {e}")

    async def _emit_normalization_status(self, __event_emitter__, applied_fixes: List[str] = None):
        """
        发送内容规范化完成的状态提示
        """
        description = "✓ 内容已自动规范化"
        if applied_fixes:
            description += f"：{', '.join(applied_fixes)}"

        try:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": description,
                        "done": True,
                    },
                }
            )
        except Exception as e:
            print(f"发送规范化状态提示时出错: {e}")

    def _contains_html(self, content: str) -> bool:
        """
        检测内容是否包含 HTML 标签
        """
        # 匹配常见的 HTML 标签
        pattern = r"<\s*/?\s*(?:html|head|body|div|span|p|br|hr|ul|ol|li|table|thead|tbody|tfoot|tr|td|th|img|a|b|i|strong|em|code|pre|blockquote|h[1-6]|script|style|form|input|button|label|select|option|iframe|link|meta|title)\b"
        return bool(re.search(pattern, content, re.IGNORECASE))

    def outlet(self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None) -> dict:
        """
        处理传出响应体，通过修改最后一条助手消息的内容。
        使用 ContentNormalizer 进行全面的内容规范化。
        """
        if "messages" in body and body["messages"]:
            last = body["messages"][-1]
            content = last.get("content", "") or ""
            
            if last.get("role") == "assistant" and isinstance(content, str):
                # 如果包含 HTML，跳过规范化，为了防止错误格式化
                if self._contains_html(content):
                    return body

                # 初始化规范化器
                normalizer = ContentNormalizer()
                
                # 执行规范化
                new_content = normalizer.normalize(content)
                
                # 更新内容
                if new_content != content:
                    last["content"] = new_content
                    # 如果内容发生了改变，发送状态提示
                    if __event_emitter__:
                        import asyncio
                        try:
                            # 传入 applied_fixes
                            asyncio.create_task(self._emit_normalization_status(__event_emitter__, normalizer.applied_fixes))
                        except RuntimeError:
                            # 假如不在循环中，则忽略
                            pass
        
        return body
