
from langchain import hub
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool,tool
from langchain_openai import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute,load_agent_executor,load_chat_planner

prompt = hub.pull("ih/ih-react-agent-executor")
prompt.pretty_print()


# 构造聊天引擎
llm = ChatOpenAI(model="gpt-4o-mini",openai_api_base="https://aihubmix.com/v1",openai_api_key="sk-xxxxxx")

# 构造查询工具
search = SerpAPIWrapper(serpapi_api_key = "xxxxxx")



import csv
from typing import List, Dict, Tuple


def load_sku_inventory(q):
    csv_file_path = "datas/inventory.csv"
    inventory = []
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                location = row[0]
                sku = row[1]
                quantity = int(row[2])
                # 将对象字典添加到结果列表
                inventory.append({'位置': location, '库存': quantity, 'SKU': sku})
    except Exception as e:
        print(f"发生错误: {e}")
    return inventory  # 只需一个 return

# 设置工具列表
tools= [
     # Tool(name="Search",func=search.run,description ="当大模型没有相关知识时，用于搜索知识"),
     Tool(name="SearchInventory",func=load_sku_inventory,description="当大模型需要获取仓库中库存信息时，用于仓库中检索库存信息  返回:- 一个字典，键为 SKU，值为包含库存及仓库位置的字典列表。")
]


# 加载规划器和执行器
planner = load_chat_planner(llm)
executor = load_agent_executor(llm, tools, verbose=True)
# 创建Plan and Execute代理
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)


order_json = {
    "orderNo": "O100001",
    "item_lines":[
        {
            "sku": "Iphone16",
            "qty": "7",
        },
        {
            "sku": "Iphone15",
            "qty": "9",
        }

    ],
    "shipping_address":{
        "country_code": "CN",
        "country": "中国",
        "city": "天津"
    }
}

rule_1 = "按照最近距离发货，我希望客户能最快收到包裹，不考虑运费"
rule_2 = "最小化拆单发货，我希望尽可能减少包裹数量，这样不用拆分包裹，节省运输费用"
rule_3 = "我希望整单发货，不希望拆分任何包裹，只有一个包裹发货"

# 将规则保存到一个列表中
rules = [rule_1]

order_info_str = str(order_json)
rules_info_str = "\n".join(rules)

task ="你是一个订单决策系统，请根据规则和多个仓库中的实际库存情况给予最优的出库建议，通知仓库按照客户指定的规则进行发货。以下是订单信息\n{},以下是规则信息\n{},订单中包含了所需的SKU和数量请严格遵守规则若规则无法满足请告诉我订单拆分异常"
filled_task = task.format(order_info_str, rules_info_str)

agent.run(filled_task)