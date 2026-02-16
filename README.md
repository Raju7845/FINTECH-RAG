# FinRAG — Indian Mutual Fund Intelligence

> FinRAG is a small RAG (retrieval-augmented generation) prototype that lets you query an indexed dataset of Indian mutual funds via a Streamlit chat UI.

## Purpose

FinRAG is built as a lightweight prototype to help analysts, data scientists, and retail investors quickly explore and query a large dataset of Indian mutual funds using natural language. It demonstrates a practical RAG workflow: converting structured CSV records into text documents, indexing them with a vector store (Chroma), and combining retrieved context with an LLM (Groq) to generate concise, analyst-style answers. FinRAG is intended for research and prototyping only — it is not financial advice.

## Project structure

- `app.py`: Streamlit frontend (chat UI and init button).
- `analytics.py`: CSV loader and converter to text documents.
- `rag_engine.py`: Vector DB helpers using Chroma and GroQ LLM integration.
- `data/`: source dataset(s) — `mutual_funds.csv`.
- `chroma_db/`: persistent Chroma vector DB files (created when initializing).

## Quick start

Prerequisites: Python 3.10+ and `pip`.

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install streamlit pandas chromadb sentence-transformers groq python-dotenv
```

3. Add your Groq API key in a `.env` file at the project root. The app reads `GROQ_API_KEY` from environment variables. Do NOT commit secrets.

```
GROQ_API_KEY=your_api_key_here
```

4. Run the Streamlit app:

```powershell
streamlit run app.py
```

Open the URL shown by Streamlit in your browser.

## How it works (high level)

- `app.py` loads the dataset via `load_data()` from `analytics.py` and shows a simple chat UI.
- When you press **Initialize RAG Database**, the app calls `convert_to_documents()` (from `analytics.py`) to transform rows into plain text documents and then `store_documents()` (from `rag_engine.py`) to add them to a persistent Chroma collection stored under `chroma_db/`.
- User queries are answered by `ask_question()` in `rag_engine.py`, which:
  - Performs an approximate search over the vector collection (via Chroma).
  - Assembles the returned documents as context for a prompt.
  - Calls the Groq API to generate a concise, financial-analyst-style response.

## Environment & keys

- The app expects `GROQ_API_KEY` to be available via environment or a `.env` file. Keep your key secret.
- If you need to run outside Streamlit or reinitialize the DB, you can run the functions directly from a short script or REPL:

```python
from analytics import load_data, convert_to_documents
from rag_engine import store_documents

df = load_data()
docs = convert_to_documents(df)
store_documents(docs)
```

## Data

The main dataset is `data/mutual_funds.csv`. It contains mutual fund records with columns such as `Scheme_Name`, `AMC`, `NAV`, `Average_AUM_Cr`, `Launch_Date`, etc. The project currently filters for `Scheme_Type == "Open Ended"` when creating documents.

## Chroma DB

- Persistent files live in `chroma_db/`. If you want to rebuild the vector index, stop the app and remove the `chroma_db/` folder contents, then re-run the initialization step.

## Notes & caveats

- The prompt in `rag_engine.py` imposes strict rules to avoid hallucination; nevertheless, validate critical recommendations before acting on them.
- The project stores a local DB and may contain sensitive information — handle the `.env` and DB files carefully.

## Next steps (suggestions)

- Add a `requirements.txt` for reproducible installs.
- Add unit tests for `analytics.py` parsing and `rag_engine.py` query handling.
- Add a script or CLI to initialize/rebuild the vector DB outside Streamlit.

---
Project generated README — edit as needed.
