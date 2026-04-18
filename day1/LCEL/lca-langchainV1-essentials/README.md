# 🔗 LangChain Essentials Python


## 🚀 Setup 

### Prerequisites

- Google Colab ( Works with any google account)
- GROQ API key

### Running on Google Colab

You can run the notebooks directly in Google Colab. The recommended Colab setup installs the required dependencies from the repository requirements file and sets up optional Node.js tooling for MCP-based lessons.

Quick Colab setup cell (paste into a Colab code cell):

```python
# Install Python dependencies from the repo
!pip install -q -r https://raw.githubusercontent.com/langchain-ai/lca-langchainV1-essentials/main/requirements.txt

# (Optional) Install Node.js for MCP tools used by some notebooks
!curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
!sudo apt-get install -y nodejs

# If you need to set environment variables, set them here (do NOT commit secrets)
import os
# Example: os.environ['GROQ_API_KEY'] = 'your_groq_api_key'
print('Setup complete')
```

Or install packages directly in Colab if you prefer specific versions:

```bash
!pip install -q langgraph langchain[all] langchain-openai langchain-anthropic jupyter
```

Open any notebook in Colab using the badges below.

## Mandatory Notebooks (Colab-ready)

| Notebook | Description | Colab |
|----------|-------------|-------|
| L1_fast_agent.ipynb | 🤖 Create Agent - Build an SQL agent in just a few lines | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/mandatory/L1_fast_agent.ipynb) |
| L2_messages.ipynb | 🧱 Messages - Learn how messages convey information between components | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/mandatory/L2_messages.ipynb) |
| L3_streaming.ipynb | 📡 Streaming - Reduce latency using streaming | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/mandatory/L3_streaming.ipynb) |
| L4_tools.ipynb | 🔧 Tools - Enhance your model with custom or prebuilt tools | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/mandatory/L4_tools.ipynb) |
| L6_memory.ipynb | 💾 Memory - Give your agent the ability to maintain state | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/mandatory/L6_memory.ipynb) |
| L7_structuredOutput.ipynb | 📋 Structured Output - Produce structured output from your agent | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/mandatory/L7_structuredOutput.ipynb) |

## Optional Notebooks (Colab-ready)

| Notebook | Description | Colab |
|----------|-------------|-------|
| L5_tools_with_mcp.ipynb | 🌐 MCP Tools - Use the LangChain MCP adapter to access MCP tools | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/optional/L5_tools_with_mcp.ipynb) |
| L8_dynamic.ipynb | 🎯 Dynamic Prompts - Dynamically modify the agent's system prompt | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/optional/L8_dynamic.ipynb) |
| L9_HITL.ipynb | 👥 Human-in-the-Loop - Enable interrupts for human interactions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/lab-day-1/batch2/lca-langchainV1-essentials/optional/L9_HITL.ipynb) |

### Getting Started with LangSmith

- Create a [LangSmith](https://smith.langchain.com/) account
- Create a LangSmith API key
<img width="600" alt="Screenshot 2025-10-16 at 8 28 03 AM" src="https://github.com/user-attachments/assets/e39b8364-c3e3-4c75-a287-d9d4685caad5" />
<img width="600" alt="Screenshot 2025-10-16 at 8 29 57 AM" src="https://github.com/user-attachments/assets/2e916b2d-e3b0-4c59-a178-c5818604b8fe" />

# 📚 Lessons
This repository contains nine short notebooks that serve as brief introductions to many of the most-used features in LangChain, starting with the new **Create Agent**.

---

### `L1_fast_agent.ipynb` - 🤖 Create Agent 🤖
- In this notebook, you will use LangChain’s `create_agent` to build an SQL agent in just a few lines of code.  
- It demonstrates how quick and easy it is to build a powerful agent. You can easily take this agent and apply it to your own project. 
- You will also use **LangSmith Studio**, a handy visual debugger to run, host, and explore agents.

---

### `L2-7.ipynb` - 🧱 Building Blocks 🧱
In Lessons 2–7, you will learn how to use some of the fundamental building blocks in LangChain. These lessons explain and complement `create_agent`, and you’ll find them useful when creating your own agents. Each lesson is concise and focused.

- **L2_messages.ipynb**: Learn how messages convey information between agent components.  
- **L3_streaming.ipynb**: Learn how to reduce user-perceived latency using streaming.  
- **L4_tools.ipynb**: Learn basic tool use to enhance your model with custom or prebuilt tools.  
- **L5_tools_with_mcp.ipynb**: Learn to use the LangChain MCP adapter to access the world of MCP tools.  
- **L6_memory.ipynb**: Learn how to give your agent the ability to maintain state between invocations.  
- **L7_structuredOutput.ipynb**: Learn how to produce structured output from your agent.  

---

### `L8-9.ipynb` - 🪛 Customize Your Agent 🤖
Lessons 2–7 covered out-of-the-box features. However, `create_agent` also supports both prebuilt and user-defined customization through **Middleware**. This section describes middleware and includes two lessons highlighting specific use cases.

- **L8_dynamic.ipynb**: Learn how to dynamically modify the agent’s system prompt to react to changing contexts.  
- **L9_HITL.ipynb**: Learn how to use Interrupts to enable Human-in-the-Loop interactions.
