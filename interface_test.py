import os
from dotenv import load_dotenv
from llm_sdk import LLMFactory

load_dotenv()


def select_model():
    """让用户选择要使用的模型配置"""
    print("\n请选择要使用的模型：")
    print("1. [本地] Ollama (Qwen2:1.5b)")
    print("2. [云端] DeepSeek (需配置 API Key)")
    print("3. [自定义] 手动输入参数")

    choice = input("\n请输入编号 (默认 1): ").strip() or "1"

    if choice == "1":
        return {
            "model_name": os.getenv("OLLAMA_MODEL", "qwen2:1.5b"),
            "base_url": os.getenv("OLLAMA_URL", "http://localhost:11434/v1"),
            "api_key": "ollama"
        }
    elif choice == "2":
        return {
            "model_name": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            "base_url": os.getenv("DEEPSEEK_URL"),
            "api_key": os.getenv("DEEPSEEK_API_KEY")
        }
    else:
        # 允许用户手动输入
        name = input("请输入模型名称: ")
        url = input("请输入 Base URL: ")
        key = input("请输入 API Key: ")
        return {"model_name": name, "base_url": url, "api_key": key}


def start_chat():
    # 1. 用户选择模型
    config = select_model()

    # 2. 初始化 LLM 实例
    try:
        llm = LLMFactory.create_llm(
            model_name=config["model_name"],
            base_url=config["base_url"],
            api_key=config["api_key"],
            streaming=True
        )
        print(f"\n系统 > 已成功连接到模型: {config['model_name']}")
    except Exception as e:
        print(f"\n错误 > 初始化失败: {e}")
        return

    print("========================================")
    print("   对话开始 (输入 'exit' 退出)   ")
    print("========================================")

    # 3. 对话循环
    while True:
        user_prompt = input("\n用户 > ")
        if user_prompt.lower() in ['exit', 'quit', '退出', 'q']:
            print("再见！")
            break

        if not user_prompt.strip():
            continue

        print("AI   > ", end="", flush=True)
        try:
            for chunk in llm.stream(user_prompt):
                print(chunk.content, end="", flush=True)
            print("\n")
        except Exception as e:
            print(f"\n发生错误: {e}")


if __name__ == "__main__":
    start_chat()