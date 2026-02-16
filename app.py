import streamlit as st
from analytics import load_data, convert_to_documents
from rag_engine import store_documents, ask_question

st.set_page_config(page_title="FinRAG", layout="wide")

st.title("FinRAG - Indian Mutual Fund Intelligence")

# ----------------------------
# Load Data
# ----------------------------

df = load_data()
st.write(f"Total Open Ended Funds Loaded: {len(df)}")

# ----------------------------
# Initialize Vector DB
# ----------------------------

if st.button("Initialize RAG Database"):
    docs = convert_to_documents(df)
    message = store_documents(docs)
    st.success(message)

# ----------------------------
# Chat Memory
# ----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.divider()
st.subheader("Ask Questions About Mutual Funds")

# Display old messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_query = st.chat_input("Ask about mutual funds...")

if user_query:
    # Store user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            answer = ask_question(user_query)
        st.markdown(answer)

    # Store assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })
