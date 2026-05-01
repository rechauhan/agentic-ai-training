import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time

from google.adk.models.lite_llm import LiteLlm

# Load environment variables from parent .env file
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

# https://docs.litellm.ai/docs/providers/groq
model = LiteLlm(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

root_agent = Agent(
    name="manager",
    #model="gemini-2.0-flash",
    model=model,
    description="Manager agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agents:
    - stock_analyst: For stock market and financial analysis
    - funny_nerd: For funny jokes and humorous responses
    - news_analyst: For news research and analysis

    You also have access to the get_current_time tool.
    """,
    sub_agents=[stock_analyst, funny_nerd, news_analyst],
    tools=[get_current_time],
)
