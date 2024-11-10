from langchain import hub
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute,load_agent_executor,load_chat_planner
from datetime import datetime

prompt = hub.pull("ih/ih-react-agent-executor")
prompt.pretty_print()


# 构造聊天引擎
llm = ChatOpenAI(model="gpt-4o-mini",openai_api_base="https://aihubmix.com/v1",openai_api_key="sk-xxxxxxx")

# 构造查询工具
search = SerpAPIWrapper(serpapi_api_key = "xxxxxxx")

def get_system_date(query):
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 设置工具列表
tools= [
     Tool(name="Search",func=search.run,description ="当大模型没有相关知识时，用于搜索知识"),
     Tool(name="GetSystemDate", func=get_system_date,description="获取当前系统日期和时间")
]


# 加载规划器和执行器
planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, verbose=True)
# 创建Plan and Execute代理
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)


agent.run("Shopify 的RestAPI 都支持那些认证方式？")