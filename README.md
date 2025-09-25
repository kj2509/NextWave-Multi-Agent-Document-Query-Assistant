# TalentHC / ADNOC Multi-Agent Document QA

An AI-powered assistant for querying enterprise documents (PDF/TXT/PPTX).  
Front-end in Streamlit, back-end API in FastAPI, retrieval via FAISS + OpenAI embeddings, and an agent built with LangChain.

## ✨ Features
- **Chat UI (Streamlit)** that talks to a local API endpoint.  
- **FastAPI backend** with a single `/ask` route that invokes the agent and returns plain text answers.  
- **Retrieval-Augmented Generation** over your docs using **FAISS** + **OpenAI embeddings (`text-embedding-3-small`)**.  
- **LangChain agent** (OpenAI by default; Groq commented as an alternative) with an ADNOC-focused system prompt and a retriever tool.  

## 🧭 Architecture
```
Streamlit UI ──► FastAPI /ask ──► LangChain Agent ──► Retriever (FAISS + Embeddings)
      ▲                                                     │
      └──────────────────── displays answer ◄───────────────┘
```

## 📁 Repo structure
```
app.py        # Streamlit front-end chat UI (posts to localhost:8080/ask)
main.py       # FastAPI server exposing POST /ask
agent.py      # LangChain agent + retriever tool + system prompt
vector.py     # Loaders, splitters, OpenAI embeddings, FAISS retriever (uploads/)
uploads/      # Put your .pdf, .txt, .pptx here
```

## 🔐 Environment variables (.env)
Create a `.env` file in the project root:

```
# LLM providers
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key

# LangChain / LangSmith (optional but supported by your codebase)
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_PROJECT=your_project_name
LANGSMITH_TRACING=true_or_false
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

## 🧱 Installation

**Python 3.10+** is recommended.

```bash
# 1) Clone and enter the project
git clone <your-repo-url>
cd <your-repo>

# 2) Create & activate a virtual env
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## 📂 Add documents
Place your source files in `uploads/`:
- Supported: **.pdf**, **.txt**, **.pptx**

## ▶️ How to run

### 1) Start the API (backend)
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### 2) Start the UI (front-end)
In a second terminal (same venv):
```bash
streamlit run app.py
```

## ⚙️ Configuration & Switching Models

- **Default LLM**: OpenAI (`gpt-4o-mini`) with low temperature for factual responses.  
- **Groq (optional)**: In `agent.py`, uncomment the Groq block and comment the OpenAI block to use **Llama 3.3 70B**.  
- **Embeddings**: OpenAI `text-embedding-3-small` for indexing. Requires `OPENAI_API_KEY`.

## ❓ Troubleshooting

- **UI says it can’t connect to backend**: Make sure the FastAPI server is running on **port 8080** before launching Streamlit.  
- **No answers or empty output**: Check your `.env` (OpenAI key is required for embeddings & default chat), and ensure `uploads/` has indexable files.  
- **500 from `/ask`**: The API wraps agent errors and returns HTTP 500 with “Agent failed to respond.” Inspect your server logs for the exception.
