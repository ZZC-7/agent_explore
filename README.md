# LLM Agent 开发项目

本项目基于 LangChain 封装的通用 LLM 调用接口，支持本地模型（Ollama）与云端模型（DeepSeek/OpenAI）调用，集成了具备**RAG**（本地知识库检索）和**联网搜索**能力的智能教师 Agent。

---

## 核心功能

- 多供应商支持：通用接口调用 Ollama 本地模型及所有兼容 OpenAI 协议的云端 API
- 模型接口测试：interface_test.py 支持用户选择本地或云端模型进行对话交互来测试接口
- RAG 本地知识库：基于 FAISS 向量数据库构建本地知识库，支持 PDF 和 TXT 文档检索
- 智能教师 Agent：集成 Tavily Search，优先查阅本地知识库，自动联网补充信息
- 上下文记忆：自动调用llm总结历史对话，维持长期对话连贯性
- 舒适交互体验：模型回答流式输出，实时显示工具调用状态

---

## 项目结构

```
.
├── llm_sdk/                    # LLM 调用接口
├── interface_test.py           # 模型对话测试脚本
├── teacher_agent.py            # 教师 Agent（集成知识库+联网搜索）
├── rag_service.py              # 本地知识库管理
├── my_knowledge/               # 本地知识库（用户需存入pdf/txt文档）
├── faiss_index/                # FAISS 向量索引（自动生成）
├── .env                        # 环境配置（用户创建并填写API）
├── .gitignore                  # Git 忽略配置
├── requirements.txt            # 依赖包列表
└── README.md                   # 项目说明文档
```

---

## 快速开始

### 第一步：克隆项目

```bash
git clone <repository-url>
cd <project-directory>
```

### 第二步：创建虚拟环境

Windows：
```bash
python -m venv venv
venv\Scripts\activate
```

Linux 或 Mac：
```bash
python -m venv venv
source venv/bin/activate
```

### 第三步：安装依赖

```bash
pip install -r requirements.txt
```

### 第四步：创建环境配置文件

在项目根目录创建 .env 文件：

```env
# Ollama 本地模型
OLLAMA_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen2:1.5b

# DeepSeek 云端模型
DEEPSEEK_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=deepseek-chat

# Tavily 联网搜索
TAVILY_API_KEY=your_api_key_here
```

获取 API Key：
- DeepSeek API: https://platform.deepseek.com
- Tavily Search API: https://tavily.com

### 第五步：启动本地模型（可选）

如果使用 Ollama：

```bash
ollama run qwen2:1.5b
```

### 第六步：准备知识库（可选）

创建并放入文档：

```bash
mkdir my_knowledge
# 将 PDF 或 TXT 文档放入该文件夹
```

### 第七步：运行程序

通用对话测试：
```bash
python interface_test.py
```

启动教师 Agent：
```bash
python teacher_agent.py
```

---

## 脚本说明

### interface_test.py

通用 LLM 对话工具，用于测试接口，支持本地/云端模型。

使用方法：
```bash
python interface_test.py
```

按提示选择模型，然后开始对话。输入 exit 或 quit 退出。

### teacher_agent.py

智能教师 Agent，集成知识库检索和联网搜索。

使用方法：
```bash
python teacher_agent.py
```

输入问题后，系统会实时显示查阅状态。输入 q 或 quit 退出。

实时状态示例：
```
学生问 > 多智能体最新进展
教师答 >
我来为您查询多智能体系统的最新进展。
[正在查阅本地文档...][✓]让我再搜索一下更具体的最新进展信息：
[正在联网搜索...][✓]基于我查询到的信息，以下是多智能体系统的最新进展：
……（流式输出）
```

### rag_service.py

本地知识库管理，支持 PDF 和 TXT 文档。

功能：
- 自动加载 my_knowledge/ 文件夹中的文档
- 构建 FAISS 向量索引
- 提供检索接口

---

## 配置说明

### 选择 LLM 模型

| 模型 | 优点 | 场景 |
|------|------|------|
| Ollama (本地) | 免费、隐私、快速 | 测试、开发 |
| DeepSeek | 性能好、价格便宜 | 生产环境 |
| OpenAI | 最强能力 | 对质量要求高 |

### 模型性能建议

- Teacher Agent：需要 7B 以上模型，推荐使用 DeepSeek
- Interface Test：支持任意模型，1.5B 也可以

---

## 常见问题

### Q1: 运行时出现 502 错误

原因：VPN 或代理干扰了本地模型连接。

解决方案：在脚本开头添加

```python
import os
os.environ["NO_PROXY"] = "localhost"
```

### Q2: FAISS 索引加载失败

原因：版本不兼容或索引文件损坏。

解决方案：删除旧索引，重新生成

```bash
rm -rf faiss_index/
python teacher_agent.py
```

### Q3: 下载 Hugging Face 模型缓慢

问题：首次启动时下载 sentence-transformers 模型较慢。

解决方案：设置 HF_TOKEN（可选，仅用于加快下载）

第一步：获取 Token

访问 https://huggingface.co/settings/tokens

点击 "New token" 按钮，创建一个新的访问令牌：
- Token name: 填任意名称（如 "my_app"）
- Role: 选择 "Read"
- 点击 "Generate a token"
- 复制生成的 Token

第二步：设置环境变量

Windows：
```bash
set HF_TOKEN=your_token_here

Linux 或 Mac：
```bash
export HF_TOKEN=your_token_here
```

### Q4: 教师 Agent 无法调用工具

原因：使用了过小的本地模型，无法理解工具调用逻辑。

解决方案：使用更大的本地模型或云端模型，1.5B 模型可能无法正确理解工具调用。

---

## 依赖清单

主要依赖包及版本：

| 包名 | 版本 | 说明 |
|------|------|------|
| langchain | 0.1.14 | LLM 框架 |
| langchain-community | 0.0.34 | 集成工具 |
| openai | 1.3.8 | API 调用 |
| sentence-transformers | 2.2.2 | 文本向量化 |
| faiss-cpu | 1.7.4 | 向量检索 |
| pypdf | 4.0.1 | PDF 处理 |
| tavily-python | 0.3.10 | 联网搜索 |
| python-dotenv | 1.0.0 | 环境配置 |

完整列表见 requirements.txt。

---

## 使用示例

### 示例一：模型对话

```bash
python interface_test.py
```

选择模型，输入问题，获得回答。

### 示例二：教学问答

```bash
python teacher_agent.py
```

输入：Python 中的装饰器是什么?
系统会实时检索本地知识库（如有）和互联网资料，流式输出答案。

### 示例三：添加自己的知识库

```bash
mkdir my_knowledge
```

放入 PDF 或 TXT 文档：
```
my_knowledge/
  ├── math_notes.pdf
  ├── physics.txt
  └── chemistry.pdf
```

运行 teacher_agent.py，系统自动构建索引。

---

## 进阶配置

### 自定义 Agent 提示词

编辑 teacher_agent.py 中的 ChatPromptTemplate 系统提示词，定义模型身份。

### 调整文档切分参数

编辑 rag_service.py 中的 build_vector_store 方法：

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,      # 增大包含更多上下文
    chunk_overlap=100    # 增大改进相似度匹配
)
```

---

## 相关资源

- LangChain 文档: https://python.langchain.com/
- Ollama 官网: https://ollama.ai
- DeepSeek API: https://platform.deepseek.com
- Tavily Search: https://tavily.com
- FAISS 文档: https://faiss.ai
---

最后更新：2026-03-31
维护者：ZZC-7