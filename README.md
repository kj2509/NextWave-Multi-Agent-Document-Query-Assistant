# NextWave Multi‑Agent Document Query Assistant

An enterprise‑style multi‑agent assistant for querying documents (PDF, TXT, PPTX).  
This repo uses a **frontend / backend / shared** layout for clean separation of UI and API logic.

---

## 🚀 Features
- **FastAPI backend** exposing `/ask` for question answering over your document corpus.
- **Streamlit frontend** that chats with the backend.
- **Retrieval‑Augmented Generation (RAG)** using FAISS + OpenAI embeddings.
- **LangChain agent** with optional Groq support.
- **Modular structure** with room for shared utilities.

---

## 📦 Repository Structure

```
backend/                 # API, agent logic, vector store setup, .env loading
  main.py                # FastAPI app entrypoint (uvicorn main:app --port 8080)
frontend/                # UI layer (Streamlit)
  app.py                 # Streamlit entry (streamlit run app.py)
shared/                  # (optional) shared utilities/configs used by both sides
  agent.py               # Agent + tools (retriever) + system prompt
  vector.py              # Loaders, splitters, embeddings, FAISS index
uploads/                 # Place your source docs here: .pdf, .txt, .pptx
requirements.txt
README.md
```

> If you migrated from a flat layout, you can use the provided `restructure.sh` to create folders and move files accordingly.

---

## 🔐 Environment Variables

Create a `.env` at the **project root** (and/or ensure your backend loads from here):

```
# LLM providers
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key

# LangChain / LangSmith (optional)
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_PROJECT=your_project_name
LANGSMITH_TRACING=false
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

- **OPENAI_API_KEY** is required for embeddings (default: `text-embedding-3-small`) and the default chat model.
- **GROQ_API_KEY** is optional if you switch to Groq/Llama models in `backend/agent.py`.

---

## 🧰 Installation

> Python **3.10+** recommended.

```bash
# 1) Clone & enter
git clone https://github.com/kj2509/NextWave-Multi-Agent-Document-Query-Assistant.git
cd NextWave-Multi-Agent-Document-Query-Assistant

# 2) (Optional) Create a venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install deps
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📂 Add Documents

Place `.pdf`, `.txt`, and `.pptx` files under `uploads/`. The backend will index them into FAISS on demand (or at startup, depending on your implementation).

---

## ▶️ Running

Open **two terminals** (same venv).

### 1) Start the backend (API)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```
- Exposes `POST /ask` that accepts JSON: `{"question": "..."}` and returns `{"answer": "..."}`.

### 2) Start the frontend (UI)
```bash
cd frontend
streamlit run app.py
```
- The UI should call `http://localhost:8080/ask` by default. Update the URL in `frontend/app.py` if you change ports/hosts.

---

## 🔄 Switching Models

- **Default**: OpenAI chat model (configured in `backend/agent.py`), low temperature for factual responses.
- **Groq**: Uncomment the Groq block in `backend/agent.py` and set `GROQ_API_KEY` in `.env`.
- **Embeddings**: OpenAI `text-embedding-3-small` by default; ensure `OPENAI_API_KEY` is set.

---

## ❓ Troubleshooting

- **Frontend cannot connect to backend**  
  Ensure the FastAPI server is running on **port 8080** before launching Streamlit, or update the frontend URL.

- **Empty or no answers**  
  Verify `.env` variables and that `uploads/` contains readable documents.

- **HTTP 500 from `/ask`**  
  Check backend logs; exceptions inside agent/retriever will bubble up. Make sure your keys are valid and models available.

---

## 🛠 Optional: Restructure from Flat Layout

If your repo has `main.py`, `app.py`, `agent.py`, `vector.py` at root, run:

```bash
bash restructure.sh
```

This will create `backend/` and `frontend/` and move files accordingly. Review the script before running.

---


