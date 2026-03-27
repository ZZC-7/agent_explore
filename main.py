# main.py
import os
from dotenv import load_dotenv
from llm_sdk import LLMFactory  # 导入你写的包

# 加载环境变量
load_dotenv()

def test_local_model():
    print("--- 测试本地 Ollama (Qwen) ---")
    # 用户只需要调用你的工厂类
    llm = LLMFactory.create_llm(
        model_name="qwen2:1.5b",
        base_url=os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
    )

    res = llm.invoke("你好，请问你是谁？")
    print(f"回答: {res.content}\n")


def test_deepseek():
    print("--- 测试云端 DeepSeek ---")
    # 如果用户想换成 DeepSeek，只需改参数
    llm = LLMFactory.create_llm(
        model_name="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_URL")
    )

    res = llm.invoke("写一段Python代码")
    print(f"回答: {res.content}")
    print("（此处需配置有效API Key才能运行）\n")


if __name__ == "__main__":
    # test_local_model()
    test_deepseek()