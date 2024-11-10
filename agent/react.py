from langchain import hub
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor

# 引入提示此模板
prompt = hub.pull("hwchase17/react")

# 构造聊天引擎
model = ChatOpenAI(model="gpt-4o-mini",openai_api_base="https://aihubmix.com/v1",openai_api_key="sk-xxxxxxxxxxxxx")

# 构造查询工具
search = SerpAPIWrapper(serpapi_api_key = "xxxxxxxxxxx")

# 设置工具列表
tools= [
     Tool(name="Search",func=search.run,description ="当大模型没有相关知识时，用于搜索知识")
]
# 构造一个 react Agent
agent = create_react_agent(model,tools,prompt)
# 构造一个 Agent 执行器
agent_executor = AgentExecutor(agent = agent,tools = tools,verbose = True)
# 执行
agent_executor.invoke({"input":"2025年美国总统是谁?"})
