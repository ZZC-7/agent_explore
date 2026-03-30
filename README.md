# 🚀 LLM Agent 开发项目

本项目基于LangChain封装的通用**llm调用接口**,支持本地模型（Ollama）与云端模型（DeepSeek/OpenAI）调用，还集成了一个具备联网搜索能力的**智能教师Agent**。拓展功能正在持续开发和更新……

## ✨ 核心功能

*   **多供应商支持**：通过统一接口调用 `Ollama` 本地模型及所有兼容 `OpenAI` 协议的云端 API。
*   **交互式模型选择**：` interface_test.py` 支持用户自主选择本地或云端模型，支持自主交互和流式输出。
*   **智能教师 Agent**：`teacher_agent.py` 集成 `Tavily Search`，当知识储备不足时会自动联网查阅资料。
*   **上下文记忆与摘要**：`memory` 模块赋予模型记忆能力（包括用户输入与模型输出），并另外调用llm对记忆内容进行总结摘要。

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
## 🤖 教师 Agent 工作流程

### 1. 加载背景 ：
在处理新问题前，Agent 首先从 ConversationSummaryMemory 中读取之前的对话摘要，确保理解当前对话的上下文。
### 2. 接收问题 ：
用户输入学科问题,Agent 结合历史摘要理解问题中的代词或隐含背景。
### 3. 判断逻辑 ：
Agent 进行逻辑分析,若问题涉及实时事实、最新科研进展或模型自身不确定的知识，将触发 ** Tavily ** 联网搜索工具。
### 4. 联网搜索 ：
Agent 自动生成精准的搜索关键词，并抓取互联网上最相关的网页核心资料。
### 5. 整合回答：
LLM 综合阅读搜索到的实时资料，并结合历史对话摘要与自身知识库，生成逻辑严密、易于理解的教学回答。
### 6. 流式输出：
通过异步任务，实时过滤Markdown形式字符，将纯文本回答流式输出到终端。
### 7. 总结记忆 ：
对话结束后，系统自动调用 LLM 对本次“用户提问 + 模型回答”进行总结，更新对话摘要并存入内存，为下一轮对话储备上下文。

### ⚠️ 注意事项

代理冲突：若运行本地模型报 502 错误，请关闭 VPN 或在代码中设置 os.environ["NO_PROXY"] = "localhost"。

模型能力：Agent 模式建议使用 DeepSeek 或 Qwen2-7B 以上模型，1.5B 模型可能无法正确处理工具调用逻辑。
