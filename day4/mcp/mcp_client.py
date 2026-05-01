import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv() # take environment variables from .env

async def main():
    print("main: start")
    
    # Get the absolute path to the math server (works on Windows and Unix)
    math_server_path = os.path.join(os.path.dirname(__file__), "math_server.py")
    print("main: math_server_path =", math_server_path)
    
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": [math_server_path],
            },
            "weather": {
                "transport": "streamable_http",
                "url": "http://localhost:8000/mcp",
            },
        }
    )
    print("main: client created")

    try:
        print("main: getting tools (10s timeout)...")
        tools = await asyncio.wait_for(client.get_tools(), timeout=10)
        print("main: got tools:", tools)
    except asyncio.TimeoutError:
        print("ERROR: client.get_tools() timed out. Is math_server or weather endpoint available?")
        return
    except Exception as e:
        print("ERROR: client.get_tools() raised:", repr(e))
        import traceback
        traceback.print_exc()
        return

    try:
        print("main: creating llm/agent")
        llm = ChatGroq(model="qwen/qwen3-32b")
        agent = create_agent(llm, tools)
        print("main: agent created")
    except Exception as e:
        print("ERROR: creating agent failed:", repr(e))
        import traceback
        traceback.print_exc()
        return

    try:
        print("main: invoking math (20s timeout)...")
        math_response = await asyncio.wait_for(
            agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}),
            timeout=20,
        )
        print("Math response:", math_response['messages'][-1])
    except asyncio.TimeoutError:
        print("ERROR: math invocation timed out")
    except Exception as e:
        print("ERROR: math invocation raised:", repr(e))
        import traceback
        traceback.print_exc()

    try:
        print("main: invoking weather (20s timeout)...")
        weather_response = await asyncio.wait_for(
            agent.ainvoke({"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}),
            timeout=20,
        )
        print("Weather response:", weather_response['messages'][-1])
    except asyncio.TimeoutError:
        print("ERROR: weather invocation timed out")
    except Exception as e:
        print("ERROR: weather invocation raised:", repr(e))
        import traceback
        traceback.print_exc()

    print("main: done")

if __name__ == "__main__":
    asyncio.run(main())