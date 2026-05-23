# Production Multi-Agent Cease & Desist Engine (Google ADK + Groq)

This system reads all incoming document streams from `sample_folder`, chunks and files them inside a custom Vector DB layer (RAG architecture), and evaluates them using dedicated specialist agents.

## Design Highlights
- **100% Google ADK Structural Alignment**: Implements isolated agent nodes with strict domain separation.
- **Multimodal Folder Scans**: Iterates seamlessly across multiple document text layers in a target directory.
- **Flawless Compliance Logs**: Splices relational databases, flat logs, and isolated JSON audit maps.
