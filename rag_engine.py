import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ----------------------------
# Create collection (helper)
# ----------------------------

def get_collection():
    client = chromadb.PersistentClient(path="./chroma_db")

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="mf_collection",
        embedding_function=embedding_function
    )

    return collection


# ----------------------------
# Store Documents (Batch Insert)
# ----------------------------

def store_documents(docs):

    collection = get_collection()

    if collection.count() > 0:
        return "Vector DB already initialized."

    batch_size = 500
    total_docs = len(docs)

    for i in range(0, total_docs, batch_size):

        batch_docs = docs[i:i + batch_size]
        batch_ids = [f"id_{j}" for j in range(i, i + len(batch_docs))]

        collection.add(
            documents=batch_docs,
            ids=batch_ids
        )

    return f"Stored {total_docs} documents successfully."


# ----------------------------
# RAG Query
# ----------------------------

def ask_question(query):

    collection = get_collection()

    if collection.count() == 0:
        return "Vector database is empty. Please initialize first."

    results = collection.query(
        query_texts=[query],
        n_results=20
    )

    if not results["documents"] or not results["documents"][0]:
        return "No relevant documents found."

    context = "\n".join(results["documents"][0])

    prompt = f"""
You are a professional financial analyst.

STRICT RULES:
1. Only use Scheme Name exactly as written.
2. Do NOT invent fund names.
3. If asked for best, compare NAV or AUM.
4. Be concise.

Mutual Fund Records:
{context}

Question:
{query}
"""

    client_groq = Groq(api_key=GROQ_API_KEY)

    response = client_groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()
