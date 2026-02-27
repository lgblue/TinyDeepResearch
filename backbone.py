from langchain_openai import ChatOpenAI
import os
from langgraph.prebuilt import create_react_agent
os.environ["OPENAI_API_KEY"] = ""

class LLMClient:
    def __init__(self):
         self.client = ChatOpenAI(
            model="Qwen/Qwen3-8B",
            # base_url="https://api.siliconflow.cn/v1",
        )

    def generate_response(self, query, tools, prompt="You are a helpful assistant"):
        agent = create_react_agent(
            model=self.client,  
            tools=tools,  
            prompt=prompt
        )
        res = agent.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        return res['messages'][-1].content