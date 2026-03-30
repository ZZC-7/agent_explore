# 🚀 LLM Agent 开发项目

本项目基于LangChain封装的通用**llm调用接口**,支持本地模型（Ollama）与云端模型（DeepSeek/OpenAI）调用，还集成了一个具备联网搜索能力的**智能教师Agent**。拓展功能正在持续开发和更新……

## ✨ 核心功能

*   **多供应商支持**：通过统一接口调用 `Ollama` 本地模型及所有兼容 `OpenAI` 协议的云端 API。
*   **交互式模型选择**：` interface_test.py` 支持用户自主选择本地或云端模型，支持自主交互和流式输出。
*   **智能教师 Agent**：`teacher_agent.py` 集成 `Tavily Search`，当知识储备不足时会自动联网查阅资料。
*   **异步流式输出**：基于 `astream_events` 实现了模型回答的流式输出，仅展示最终回答，隐藏中间思考过程。
*   **纯文本格式**：内置正则过滤引擎，自动剔除 Markdown 符号（如 `###`, `**`），提供整洁的阅读体验。

## 📂 项目结构

*   `llm_sdk/`：核心封装包，提供llm调用接口。
*   `interface_test.py`：模型对话测试脚本，支持模型调用选择与流式交互。
*   `teacher_agent.py`：教师Agent脚本，具备联网搜索与异步流式功能。
*   `.env`：环境配置文件，管理 API_Key 和 URL（用户需要手动创建）。
*   `.gitignore`：配置文件，确保敏感信息（如 `.env`）不被上传。

## 🛠️ 快速开始

### 1. 安装依赖
在终端运行以下命令安装核心库：
```bash
pip install langchain langchain-openai langchain-community python-dotenv tavily-python
```
### 2. 环境配置

在项目根目录创建 .env 文件，并填入你的配置：

```text
# 本地 Ollama 配置
OLLAMA_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2:1.5b

# 云端 DeepSeek 配置
DEEPSEEK_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=your_api_key
DEEPSEEK_MODEL=deepseek-chat

# 联网搜索配置 (去 tavily.com 免费获取)
TAVILY_API_KEY=your_api_key
```
### 3. 启动本地模型

如果你想使用本地模型，请确保 Ollama 已启动并下载了模型：

```bash
ollama run qwen2:1.5b
```
### 4. 运行程序

运行通用对话脚本，测试llm调用接口：
```bash
python main.py
```
运行教师 Agent 脚本：
```bash
python teacher_agent.py
```
### 🤖 教师 Agent 工作流程

接收问题：用户输入学科问题。

判断逻辑：Agent 分析问题，若涉及实时事实或复杂知识，触发 Tavily 搜索工具。

联网搜索：自动生成关键词并抓取网页核心资料。

整合回答：LLM 阅读搜索结果，结合自身知识库，生成易于理解的教学回答。

流式展示：通过异步任务，实时过滤 Markdown 杂质，将纯净文字推送到终端。

### ⚠️ 注意事项

代理冲突：若运行本地模型报 502 错误，请关闭 VPN 或在代码中设置 os.environ["NO_PROXY"] = "localhost"。

模型能力：Agent 模式建议使用 DeepSeek 或 Qwen2-7B 以上模型，1.5B 模型可能无法正确处理工具调用逻辑。
