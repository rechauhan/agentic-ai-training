# Model Context Protocol (MCP) - Practical Implementation

## Overview

This directory contains hands-on examples of the **Model Context Protocol (MCP)**, demonstrating how to:
1. **Create MCP servers** that expose tools (math operations, weather data)
2. **Connect multiple MCP servers** to a single client
3. **Use LangChain agents** to automatically call tools via MCP
4. **Integrate with LLMs** to enable AI-powered tool usage

This is a practical, beginner-friendly introduction to MCP without external service dependencies.

## What is MCP?

**MCP (Model Context Protocol)** is a standard that allows AI models to:
- **Discover available tools** from servers
- **Call tools** to perform actions
- **Receive results** in a structured format
- **Chain multiple operations** across different servers

Think of MCP as a **plug-and-play system** for giving AI models access to external capabilities.

## Key Concepts

### 1. **MCP Server**
A server that exposes tools the AI model can use:
```python
from fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

### 2. **MCP Client**
A client that connects to multiple servers and orchestrates tool calls:
```python
client = MultiServerMCPClient({
    "math": {"transport": "stdio", "command": "python", "args": ["math_server.py"]},
    "weather": {"transport": "streamable_http", "url": "http://localhost:8000/mcp"}
})
tools = await client.get_tools()
```

### 3. **Tool Definition**
A function decorated with `@mcp.tool()` that becomes available to AI models:
```python
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
```

### 4. **Transport Mechanism**
How the client communicates with servers:
- **stdio**: Standard input/output (for local Python processes)
- **streamable_http**: HTTP endpoints (for web-based servers)

## File Structure

```
day4_mcp/
├── README.md                 # This file
├── math_server.py           # MCP Server exposing math tools (add, multiply)
├── weather_server.py        # MCP Server exposing weather tool
├── mcp_client.py            # Client connecting both servers + LLM integration
└── requirements.txt         # Dependencies
```

## Prerequisites

### Required Knowledge
- **Python Basics**: Functions, decorators, async/await
- **REST APIs**: Basic understanding of HTTP
- **Agentic AI**: From previous LCEL training
- **LLMs**: How language models work with tools

### Required Installations
```bash
pip install fastmcp langchain-mcp-adapters langchain-groq python-dotenv langchain
```

## How It Works

### Step 1: MCP Server Starts
```
math_server.py → Exposes: add(), multiply() tools
weather_server.py → Exposes: get_weather() tool
```

### Step 2: MCP Client Discovers Tools
```
mcp_client.py → Connects to both servers
             → Gets list of available tools
             → Registers with LangChain
```

### Step 3: LLM Uses Tools
```
User: "What's (3 + 5) × 12?"
      ↓
LLM: "I need to add 3+5 first, then multiply by 12"
      ↓
Call: add(3, 5) → 8 (via math_server)
Call: multiply(8, 12) → 96 (via math_server)
      ↓
Response: "The answer is 96"
```

## Quick Start

### 1. Start the Math Server
```bash
python math_server.py
```
This starts an MCP server on stdio, exposing:
- `add(a: int, b: int)` - Add two numbers
- `multiply(a: int, b: int)` - Multiply two numbers

### 2. Start the Weather Server (in another terminal)
```bash
python weather_server.py
```
This starts an HTTP server on `http://localhost:8000/mcp`, exposing:
- `get_weather(location: str)` - Get weather for a location

### 3. Run the Client
```bash
# Set up environment variable
export GROQ_API_KEY=your_key_here

# Run the client
python mcp_client.py
```

The client will:
- Connect to both servers
- Discover all available tools
- Create a LangChain agent
- Ask the agent math and weather questions
- Display responses

## Code Walkthrough

### math_server.py
```python
# ...existing imports...
mcp = FastMCP("Math")  # Create MCP server named "Math"

@mcp.tool()  # Decorator makes function available as a tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

# ...run on stdio transport...
```

**Key Points:**
- Type hints (`a: int, b: int`) are required for MCP schema
- Docstrings describe what the tool does
- `transport="stdio"` means it communicates via stdin/stdout

### weather_server.py
```python
# ...similar to math_server...
mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "It's always sunny in New York"

# ...run on streamable_http transport...
```

**Key Points:**
- Can be async (optional)
- `transport="streamable_http"` exposes HTTP endpoint
- Returns string directly (LLM will use this in responses)

### mcp_client.py
```python
# Create client connecting to both servers
client = MultiServerMCPClient({
    "math": {
        "transport": "stdio",
        "command": "python",
        "args": [math_server_path],
    },
    "weather": {
        "transport": "streamable_http",
        "url": "http://localhost:8000/mcp",
    },
})

# Get all tools from both servers
tools = await client.get_tools()

# Create LangChain agent with tools
llm = ChatGroq(model="qwen/qwen3-32b")
agent = create_agent(llm, tools)

# Agent automatically calls appropriate tools
response = await agent.ainvoke({
    "messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]
})
```

**Key Points:**
- `MultiServerMCPClient` manages multiple servers
- `await client.get_tools()` discovers all available tools
- LangChain agent automatically selects and calls tools
- Works with any Groq/LLM model

## Common Patterns

### Pattern 1: Simple Tool Definition
```python
@mcp.tool()
def calculator_tool(expression: str) -> float:
    """Evaluate a mathematical expression"""
    return eval(expression)
```

### Pattern 2: Tool with Multiple Parameters
```python
@mcp.tool()
def search_database(query: str, limit: int = 10) -> list:
    """Search database with optional limit"""
    # Implementation here
    return results
```

### Pattern 3: Tool Returning Structured Data
```python
@mcp.tool()
def get_user_info(user_id: int) -> dict:
    """Get user information"""
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com"
    }
```
