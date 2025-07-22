# GenAI Cohort 🚀

A collection of modular projects and experiments exploring Generative AI concepts and applications. This repository is structured to guide you through key GenAI workflows step by step — from basic tokenization to advanced Retrieval-Augmented Generation (RAG), LangGraph flows, and human-in-the-loop systems.

---

## 📦 Project Structure

| Module                 | Description                                                   |
| ---------------------- | ------------------------------------------------------------- |
| `01_tokenization`      | Introduction to tokenization in NLP pipelines.                |
| `02_vector_embeddings` | Working with vector embeddings for semantic understanding.    |
| `04_rag`               | Retrieval-Augmented Generation (RAG) pipeline implementation. |
| `05_rag_queue`         | Advanced RAG pipeline with queuing for scalability.           |
| `06_langraph`          | Building and visualizing workflows with LangGraph.            |
| `07_chat_graph`        | Creating conversational agents using graph-based workflows.   |
| `08_human_in_loop`     | Integrating human feedback into AI decision loops.            |
| `08_tools`             | Utility tools to support GenAI workflows.                     |
| `09_memory`            | Techniques for adding memory to conversational agents.        |
| `web_loader`           | Loading and scraping web content for downstream tasks.        |
| `.devcontainer`        | Development container setup for consistent environments.      |

---

## 🛠️ Setup

Clone the repository:

```bash
git clone https://github.com/ridamsinghal25/genai.git
cd genai
```

Install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 How to Run

Each module is independent. Navigate to any module and run its main script or notebook:

```bash
cd 04_rag
python main.py
```

---
