# llm_sdk/factory.py
from langchain_openai import ChatOpenAI
from typing import Optional


class LLMFactory:
    """LLM 统一调用工厂类"""

    @staticmethod
    def create_llm(
            model_name: str,
            api_key: str = "EMPTY",
            base_url: Optional[str] = None,
            temperature: float = 0.7,
            streaming: bool = False,
            **kwargs
    ) -> ChatOpenAI:
        """
        创建一个通用的 ChatOpenAI 实例
        :param model_name: 模型名称 (如 'qwen2:1.5b', 'gpt-4')
        :param api_key: API 密钥 (本地模型随便填)
        :param base_url: API 接口地址
        :param temperature: 温度参数 (0-2)
        :param streaming: 是否启用流式输出
        """
        return ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base=base_url,
            temperature=temperature,
            streaming=streaming,
            **kwargs
        )