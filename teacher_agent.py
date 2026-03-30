import os
import re
import asyncio
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationSummaryMemory  # 引入总结记忆
from llm_sdk import LLMFactory

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

    # 2. 定义工具
    search_tool = TavilySearchResults(max_results=3)
    tools = [search_tool]

    # 3. 定义教师 Persona （系统提示词）
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一位博学、耐心的资深教师。
        你的任务是回答学生关于各学科的问题。
        请结合【对话摘要】和【搜索结果】来回答。
        【重要】严禁使用Markdown格式，仅使用纯文本、数字、空格和换行符。
        请使用中文回答。"""),
        # 这里的chat_history将由memory填充，赋予模型拥有上下文记忆
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 4. 记忆总结
    memory = ConversationSummaryMemory(
        llm=llm,     # 需要一个llm来执行总结任务
        memory_key="chat_history",
        return_messages=True,
        output_key="output"  # 明确指定要记忆的是模型输出
    )

    # 5. 构造Agent
    agent = create_openai_tools_agent(llm, tools, prompt) # agent参数：模型，工具，提示词

    # 6. 构造执行器
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,  # 记忆模块
        verbose=False,
        handle_parsing_errors=True
    ), memory  # 返回执行器和记忆对象


async def start_teacher_chat():
    # 获取执行器和记忆对象
    teacher, memory = create_teacher_agent()

    print(" --> 教师Agent启动 ")

    while True:
        query = input("\n学生问 > ")
        if query.lower() in ['exit', 'q']: break

        print("教师答 > ", end="", flush=True)

        # 用于存储本次回答的完整文本来更新记忆
        full_response = ""

        try:
            async for event in teacher.astream_events({"input": query}, version="v2"):
                kind = event["event"]

                if kind == "on_chat_model_stream": # 模型回答
                    content = event["data"]["chunk"].content
                    if content:
                        # 过滤Markdown格式字符
                        clean_content = re.sub(r'[#*>\-]', '', content)
                        print(clean_content, end="", flush=True)
                        full_response += clean_content

                elif kind == "on_tool_start": # 调用工具
                    print(f"\n[正在查阅: {event['name']}...]", end="", flush=True)

            print("\n")

        except Exception as e:
            print(f"\n发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(start_teacher_chat())