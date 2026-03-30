🚀 Agent开发项目

本项目基于LangChain封装的通用大模型调用框架，不仅支持本地模型（通过 vLLM/Ollama）与云端模型（如 DeepSeek/OpenAI）的调用，还集成了一个具备联网搜索能力的智能教师 Agent。后续进阶功能持续开发更新。。。

✨ 核心功能

多供应商支持：通过统一接口调用 Ollama 本地模型及所有兼容 OpenAI 协议的云端 API。

交互式模型选择：main.py 支持在启动时动态选择本地或云端模型。

智能教师 Agent：teacher_agent.py 集成 Tavily Search，当知识储备不足时会自动联网查阅资料。

异步流式输出：基于 astream_events 实现真正的打字机效果，仅展示最终回答，隐藏中间思考过程。

纯文本格式优化：内置正则过滤引擎，自动剔除 Markdown 符号（如 ###, **），提供最整洁的阅读体验。

📂 项目结构

llm_sdk/：核心封装包，包含模型工厂类。

main.py：通用对话测试脚本，支持模型切换。

teacher_agent.py：进阶 Agent 脚本，具备联网搜索与异步流式功能。

.env：环境配置文件，管理 API Key 和 URL。

🛠️ 快速开始
1. 安装依赖
code
Bash
download
content_copy
expand_less
pip install langchain langchain-openai langchain-community python-dotenv tavily-python
2. 环境配置

在项目根目录创建 .env 文件，参考如下配置：

code
Text
download
content_copy
expand_less
# 本地 Ollama 配置
OLLAMA_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2:1.5b

# 云端 DeepSeek 配置
DEEPSEEK_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=deepseek-chat

# 联网搜索配置 (去 tavily.com 免费获取)
TAVILY_API_KEY=tvly-xxxxxxxxxxxx
3. 启动本地模型 (可选)

如果你想使用本地模型，请确保 Ollama 已启动：

code
Bash
download
content_copy
expand_less
ollama run qwen2:1.5b
4. 运行程序

普通对话模式（支持模型切换）：

code
Bash
download
content_copy
expand_less
python main.py

智能教师 Agent 模式（支持联网搜索）：

code
Bash
download
content_copy
expand_less
python teacher_agent.py
🤖 教师 Agent 工作流程

接收问题：用户输入学科问题。

判断逻辑：Agent 分析问题，若涉及实时事实或复杂知识，触发 Tavily 搜索。

联网搜索：自动生成关键词并抓取网页前 3 条核心资料。

整合回答：LLM 阅读搜索结果，结合自身知识库，生成易于理解的教学回答。

流式展示：通过异步任务，实时过滤 Markdown 杂质，将纯净的文字推送到终端。

⚠️ 注意事项

代理冲突：若运行本地模型报 502 错误，请关闭 VPN 或在代码中设置 os.environ["NO_PROXY"] = "localhost"。

模型能力：Agent 模式建议使用 DeepSeek 或 Qwen2-7B 以上模型，1.5B 模型可能无法正确处理工具调用逻辑。