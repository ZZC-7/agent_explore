import os
import re
import asyncio
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_sdk import LLMFactory

load_dotenv()

def create_teacher_agent():
    # 初始化 LLM
    llm = LLMFactory.create_llm(
        model_name="deepseek-chat", # 使用云端大型模型
        base_url=os.getenv("DEEPSEEK_URL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.1,  # 设置低温度，保证逻辑稳定
        streaming=True
    )

    # 定义工具：联网搜索
    search_tool = TavilySearchResults(max_results=3)
    tools = [search_tool]

    # 定义教师 Persona (系统提示词)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一位博学、耐心的资深教师。
        你的任务是回答学生关于各学科的问题。
        如果问题涉及最新的科学进展、具体事实或你不确定的知识，请务必使用【联网搜索工具】来获取准确资料。
        在回答时，请先总结搜索到的资料，再以易懂的方式向学生解释，并给出学习建议。
        【严禁使用Markdown格式】使用纯文本、数字、空格和换行符进行排版。
        请使用中文回答。"""),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 构造Agent
    agent = create_openai_tools_agent(llm, tools, prompt) # agent参数：模型，工具，提示词

    # 5. 构造执行器
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,  # 关闭详细日志
        handle_parsing_errors=True
    )


async def start_teacher_chat():
    teacher = create_teacher_agent()

    print(" --> 教师Agent启动 ")

    while True:
        query = input("\n学生问 > ")
        if query.lower() in ['exit', 'q']: break

        print("教师答 > ", end="", flush=True)

        try: # 流式输出
            async for event in teacher.astream_events({"input": query}, version="v2"):
                kind = event["event"]
                if kind == "on_chat_model_stream": # 模型回答用户问题
                    content = event["data"]["chunk"].content
                    if content:
                        content = re.sub(r'[#*>\-]', '', content) # 利用正则过滤Markdown格式字符，美观输出
                        print(content, end="", flush=True)


                elif kind == "on_tool_start": # 模型调用搜索工具
                     print(f"\n[正在查阅: {event['name']}...]", end="", flush=True)

            print("\n")

        except Exception as e:
            print(f"\n发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(start_teacher_chat())