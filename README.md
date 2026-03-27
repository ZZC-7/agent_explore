# My LLM Agent SDK

这是一个基于 LangChain 封装的通用 LLM 调用接口。

## 快速开始

1\. 安装依赖：`pip install langchain-openai python-dotenv`

2\. 启动本地模型：`ollama run qwen2:1.5b`

3\. 配置 `.env` 文件 设置需要调用的模型的api-key和URL

4\. 运行测试：`python main.py` 自主选择本地/云端模型，自主交互，流式输出
