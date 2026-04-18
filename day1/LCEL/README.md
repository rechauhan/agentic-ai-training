# LCEL (LangChain Expression Language) Deepdive

## Overview
This notebook provides a comprehensive guide to understanding **LangChain Expression Language (LCEL)**, a declarative way to compose chains in LangChain. LCEL is fundamental for building agentic AI systems that can reason, plan, and execute tasks.

## Prerequisites

### Required Knowledge
- **Python Basics**: Understanding of classes, functions, decorators, and lambda functions
- **Async Programming**: Basic familiarity with async/await concepts (helpful but not mandatory)
- **LLM Concepts**: Understanding of prompts, tokens, and model parameters (temperature, max_tokens, etc.)

### Required Installations
```bash
pip install -qU langchain-groq langchain_community langchain_huggingface faiss-cpu
```

### API Keys
- **Groq API Key**: Get from [Groq Console](https://console.groq.com) - Required to run LLM examples

## What is LCEL?

LCEL is a design pattern that allows you to:
1. **Compose** complex AI workflows from simple, reusable components
2. **Chain** operations together using the pipe operator (`|`)
3. **Parallelize** independent processing branches
4. **Debug** by inspecting intermediate outputs

Think of LCEL as building a data pipeline where each component transforms input into output.

## Key Concepts

### 1. **The Pipe Operator (`|`)**
```python
chain = prompt | model | output_parser
```
The pipe operator chains components sequentially. Data flows from left to right, with each component's output becoming the next component's input.

### 2. **Runnables**
A `Runnable` is any component that can process input and produce output:
- **Prompts**: Format user input into instructions for the model
- **Models**: LLMs that generate responses
- **Output Parsers**: Convert raw model output into structured data
- **Custom Functions**: Lambda functions or custom classes wrapped in `RunnableLambda`

### 3. **RunnablePassthrough**
Passes data through unchanged. Useful for:
- Preserving context in chains
- Branching data to multiple processors
- Debugging intermediate values

### 4. **RunnableLambda**
Wraps Python functions to make them composable in chains:
```python
RunnableLambda(lambda x: x.upper())
```

### 5. **RunnableParallel**
Processes the same input through multiple branches simultaneously:
```python
RunnableParallel({
    "branch1": processor1,
    "branch2": processor2
})
```
Returns a dictionary with keys matching each branch.

### 6. **Assignment with `.assign()`**
Adds computed fields to the output while preserving existing data:
```python
chain.assign(new_field=RunnableLambda(compute_function))
```

## Notebook Structure

### Section 1: Basic LCEL Chain
Demonstrates the fundamental pattern: **Prompt → Model → Output Parser**

### Section 2: Understanding the Pipe Operator
Implements a custom `Runnable` class to show how the pipe operator works internally.

### Section 3: LangChain's Built-in Runnables
Explores `RunnablePassthrough`, `RunnableLambda`, and `RunnableParallel`.

### Section 4: Nested Chains
Combines parallel and sequential processing for complex transformations.

### Section 5: Chain Composition
Shows how to combine multiple chains together (chain coercion).

### Section 6: Real-World Example (RAG)
Builds a **Retrieval-Augmented Generation** system:
1. **Retriever**: Searches a vector database for relevant documents
2. **Context Formatting**: Converts retrieved documents to readable text
3. **Prompt Injection**: Combines context + question in a prompt
4. **LLM Response**: Model generates answer based on context
5. **Output Parsing**: Extracts final response

## Why LCEL Matters for Agentic AI

Agentic AI systems need to:
- **Reason** over multiple sources of information
- **Plan** multi-step tasks with decision points
- **Execute** parallel operations efficiently
- **Adapt** based on intermediate results

LCEL provides the foundation for all of this by:
1. Making chains **composable** (mix and match components)
2. Supporting **branching** (parallel processing)
3. Enabling **introspection** (debug intermediate steps)
4. Allowing **dynamic routing** (conditional logic in chains)

## Quick Start

### 1. Set up environment
```python
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key="your-api-key"
)
```

### 2. Create a simple chain
```python
prompt = ChatPromptTemplate.from_template("Explain {topic}")
chain = prompt | model | StrOutputParser()
result = chain.invoke({"topic": "machine learning"})
```

### 3. Debug intermediate steps
```python
# See the formatted prompt
print(prompt.invoke({"topic": "machine learning"}))

# See the raw model output
print(model.invoke(prompt.invoke({"topic": "machine learning"})))
```

## Common Patterns

### Pattern 1: Context Enrichment
```python
chain = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough()
}) | prompt | model
```

### Pattern 2: Data Transformation Pipeline
```python
chain = RunnableLambda(extract) | RunnableLambda(transform) | RunnableLambda(validate)
```

### Pattern 3: Parallel Processing with Merging
```python
chain = RunnableParallel({
    "path1": processor1,
    "path2": processor2
}).assign(merged=RunnableLambda(merge_function))
```

## Learning Path for Agentic AI

1. **Master LCEL** ← You are here
   - Understand basic chains
   - Learn about Runnables
   - Practice nested chains

2. **Agents** (Next)
   - Learn ReAct (Reasoning + Acting)
   - Build agents that plan and execute
   - Implement tool calling

3. **Memory & Context**
   - Manage conversation history
   - Implement retrieval augmented generation
   - Handle long-context scenarios

4. **Multi-step Workflows**
   - Orchestrate complex agentic systems
   - Implement error handling and retries
   - Build production-grade agents

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Ensure all dependencies are installed:
```bash
pip install -qU langchain-groq langchain_community langchain_huggingface faiss-cpu
```

### Issue: API key authentication fails
**Solution**: Verify your Groq API key is set correctly:
```python
import os
os.environ["GROQ_API_KEY"] = "your-actual-api-key"
```

### Issue: Vector store initialization fails
**Solution**: Ensure HuggingFace embeddings are downloaded. The first run may take time.

## Resources

- [LangChain Documentation](https://python.langchain.com)
- [LCEL Concepts Guide](https://python.langchain.com/docs/expression_language/)
- [Groq API Documentation](https://console.groq.com/docs)
- [RAG Pattern Overview](https://python.langchain.com/docs/use_cases/question_answering/)

## Next Steps

After completing this notebook:
1. Experiment with custom Runnables
2. Build a RAG system with your own documents
3. Implement tool-calling with agents
4. Explore streaming and async patterns

---

**Happy Learning! 🚀**
