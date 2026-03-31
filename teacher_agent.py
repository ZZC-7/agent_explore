import os
import asyncio
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from llm_sdk import LLMFactory
from langchain.tools.retriever import create_retriever_tool
from rag_service import RAGService

load_dotenv()

def create_teacher_agent():
    # 1. 初始化 LLM
    llm = LLMFactory.create_llm(
        model_name="deepseek-chat",
        base_url=os.getenv("DEEPSEEK_URL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.1,
        streaming=True
    )

    # 2. 定义工具列表
    tools = []

    # 集成 RAG 本地知识库工具
    rag_service = RAGService(data_path="./my_knowledge")
    retriever = rag_service.get_retriever()

    if retriever:
        # 将检索器包装成 Agent 可以调用的 Tool
        rag_tool = create_retriever_tool(
            retriever,
            "knowledge_base_search",
            "用于查询本地教学资料库。当你需要查找特定教材内容、课件知识或内部文档时，必须优先使用此工具。"
        )
        tools.append(rag_tool)

    # 添加联网搜索工具
    search_tool = TavilySearchResults(max_results=3)
    tools.append(search_tool)

    # 3. 定义教师 Persona （系统提示词）
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一位博学、耐心的资深教师。
        你的任务是回答学生关于各学科的问题。

        【工作准则】：
        1. 优先级：如果学生的问题在【本地教学资料库】中有相关记录，请优先使用该资料库的内容进行回答。
        2. 补充：如果本地资料库无法提供完整答案，且涉及实时事实，请使用【联网搜索工具】。
        3. 结合【对话摘要】和上述工具结果进行综合解答。

        【重要】严禁使用Markdown格式，仅使用纯文本、数字、空格和换行符。
        请使用中文回答。"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 4. 记忆总结
    memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )

    # 5. 构造Agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    # 6. 构造执行器
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=False,
        handle_parsing_errors=True
    )


class CustomToolCallbackHandler(BaseCallbackHandler):
    """自定义工具调用的回调处理器"""

    def on_tool_start(self, serialized, input_str, **kwargs):
        """工具开始调用时"""
        tool_name = serialized.get("name", "")
        if tool_name == "knowledge_base_search":
            print("\n[正在查阅本地文档...]", end="", flush=True)
        elif tool_name == "tavily_search_results_json":
            print("\n[正在联网搜索...]", end="", flush=True)
        else:
            print(f"\n[正在调用: {tool_name}]", end="", flush=True)

    def on_tool_end(self, output, **kwargs):
        """工具结束时"""
        print("[✓]", end="", flush=True)


def start_teacher_chat():
    """启动教师Agent对话"""
    teacher = create_teacher_agent()
    print("\n --> 教师Agent启动 (支持本地知识库 & 联网搜索) <--")
    print("输入 'q' 或 'quit' 退出对话\n")

    while True:
        try:
            query = input("学生问 > ").strip()

            if query.lower() in ['q', 'quit']:
                print("会话已结束")
                break

            if not query:
                print("请输入问题")
                continue

            print("教师答 > \n", end="", flush=True)

            max_retries = 3
            for attempt in range(max_retries):
                try:
                    callbacks = [
                        StreamingStdOutCallbackHandler(),
                        CustomToolCallbackHandler()
                    ]

                    teacher.invoke(
                        {"input": query},
                        config={"callbacks": callbacks}
                    )

                    print("\n")
                    break

                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"\n连接中断，正在重试 ({attempt + 1}/{max_retries})...")
                        import time
                        time.sleep(2 ** attempt)
                    else:
                        print(f"\n发生错误: {e}")

        except KeyboardInterrupt:
            print("\n会话已结束")
            break


if __name__ == "__main__":
    start_teacher_chat()