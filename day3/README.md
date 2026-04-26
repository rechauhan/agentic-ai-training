# Jan'26 Batch Day 3 Labs

This repository contains the hands-on labs for Day 3 of the Agentic AI Training workshop (Jan 2026 Batch). The labs focus on **LangGraph Persistence**, **Human-in-the-Loop (HITL)** workflows, and **LLM Observability**.

## Lab List

| Lab | Topic | Description | Key Concepts | Colab Link |
| :--- | :--- | :--- | :--- | :--- |
| **Lab 3.1** | **LangGraph Persistence** | Add memory to the graph to remember state across interactions (long-running conversations). | Checkpointer, MemorySaver, Thread ID | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/main/day3/Lab3_1_LangGraph_Persistence.ipynb) |
| **Lab 3.2** | **HITL Basics** | Learn how to pause execution of a graph to allow for human intervention. | Interrupts (before/after), State Inspection, State Update, Resuming | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/main/day3/Lab3_2_LangGraph_HITL_Basics.ipynb) |
| **Lab 3.3** | **HITL Review Pattern** | Implement a "Review Tool Calls" pattern where a human must approve sensitive actions before execution. | Interrupt before tools, Inspecting Pending Tool Calls, Approve vs. Reject (state update) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/main/day3/Lab3_3_LangGraph_HITL_Review.ipynb) |
| **Lab 3.4** | **(OPTIONAL) LangGraph Adv Concepts** | Instrument LLM applications (LangChain & LangGraph) dynamic Routing, SQL Checkpointer | SQL Checkpointer, Command, Time Travel | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/main/day3/Lab3_4_Advanced_LangGraph_Concepts.ipynb) |
| **Lab 3.5** | **Observability (Arize Phoenix)** | Instrument LLM applications (LangChain & LangGraph) for observability using Arize Phoenix to trace and debug complex flows. | OpenTelemetry Traces, Arize Phoenix, Debugging LangGraph nodes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jayyanar/agentic-ai-training/blob/main/day3/Lab3_5_Arize_Phoenix.ipynb) |
