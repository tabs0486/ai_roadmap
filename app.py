"""
AI Learning Lab - one Streamlit app, three skills:
  1) Chatbot        -> LLM basics + prompting (Groq)
  2) Document Q&A   -> RAG (TF-IDF retrieval, no heavy downloads)
  3) Agent          -> tool calling (calculator, clock, your documents)

Run locally:   streamlit run app.py
"""
import ast
import json
import operator
from datetime import datetime

import streamlit as st
from groq import Groq
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Learning Lab", page_icon="🧠", layout="wide")

MODELS = [
    "llama-3.3-70b-versatile",  # best quality, good for agents
    "llama-3.1-8b-instant",     # fastest / cheapest
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]


# ---------------------------------------------------------------- Groq client
def get_client() -> Groq | None:
    key = st.session_state.get("user_key") or st.secrets.get("GROQ_API_KEY", None)
    if not key:
        return None
    return Groq(api_key=key)


# ------------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🧠 AI Learning Lab")
    page = st.radio("Choose a lab", ["💬 Chatbot", "📄 Document Q&A (RAG)", "🤖 Agent"])
    model = st.selectbox("Groq model", MODELS)
    temperature = st.slider("Temperature", 0.0, 1.5, 0.3, 0.1)
    st.text_input(
        "Groq API key (optional if set in secrets)",
        type="password",
        key="user_key",
        help="Get a free key at console.groq.com/keys",
    )
    st.caption("Keys typed here live only in your browser session.")

client = get_client()
if client is None:
    st.warning("Add your Groq API key in the sidebar (free at console.groq.com/keys) "
               "or in .streamlit/secrets.toml.")
    st.stop()


# ----------------------------------------------------------------- 1. CHATBOT
def chatbot_page():
    st.header("💬 Chatbot")
    st.write("Learn **prompting**: change the system prompt and watch behaviour change.")
    system = st.text_area(
        "System prompt",
        "You are a patient AI tutor. Explain simply, use examples, and end with one quiz question.",
        height=90,
    )
    if "chat" not in st.session_state:
        st.session_state.chat = []

    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Ask anything about AI..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=model,
                temperature=temperature,
                stream=True,
                messages=[{"role": "system", "content": system}] + st.session_state.chat,
            )
            reply = st.write_stream(
                chunk.choices[0].delta.content or "" for chunk in stream
            )
        st.session_state.chat.append({"role": "assistant", "content": reply})

    if st.button("Clear chat"):
        st.session_state.chat = []
        st.rerun()


# --------------------------------------------------------------------- 2. RAG
def read_file(f) -> str:
    if f.name.lower().endswith(".pdf"):
        return "\n".join((p.extract_text() or "") for p in PdfReader(f).pages)
    return f.read().decode("utf-8", errors="ignore")


def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    text = " ".join(text.split())
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


def build_index(files):
    chunks = []
    for f in files:
        for c in chunk_text(read_file(f)):
            chunks.append({"source": f.name, "text": c})
    if not chunks:
        return None
    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform([c["text"] for c in chunks])
    return {"chunks": chunks, "vec": vec, "matrix": matrix}


def retrieve(query: str, k: int = 4):
    idx = st.session_state.get("index")
    if not idx:
        return []
    sims = cosine_similarity(idx["vec"].transform([query]), idx["matrix"])[0]
    top = sims.argsort()[::-1][:k]
    return [(idx["chunks"][i], float(sims[i])) for i in top if sims[i] > 0]


def rag_page():
    st.header("📄 Document Q&A (RAG)")
    st.write("Upload PDFs or .txt files, then ask questions. Answers must come from your documents.")
    files = st.file_uploader("Upload documents", type=["pdf", "txt", "md"], accept_multiple_files=True)
    col1, col2 = st.columns(2)
    if col1.button("Build index", disabled=not files):
        st.session_state.index = build_index(files)
        n = len(st.session_state.index["chunks"]) if st.session_state.index else 0
        st.success(f"Indexed {n} chunks.")
    if col2.button("Use sample document"):
        with open("sample_data/sample.txt", "rb") as fh:
            fh.name = "sample.txt"
            st.session_state.index = build_index([fh])
        st.success("Sample indexed.")

    q = st.text_input("Your question")
    if q:
        hits = retrieve(q)
        if not hits:
            st.info("Build an index first, or the question has no overlap with your documents.")
            return
        context = "\n\n".join(f"[{i+1}] ({h['source']}) {h['text']}" for i, (h, _) in enumerate(hits))
        resp = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content":
                    "Answer ONLY using the numbered context. Cite sources like [1]. "
                    "If the answer is not in the context, say you don't know."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {q}"},
            ],
        )
        st.markdown(resp.choices[0].message.content)
        with st.expander("Retrieved chunks (debug your RAG here)"):
            for i, (h, score) in enumerate(hits):
                st.markdown(f"**[{i+1}] {h['source']}** - similarity {score:.2f}")
                st.caption(h["text"])


# -------------------------------------------------------------------- 3. AGENT
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
        ast.Mod: operator.mod}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


def tool_calculator(expression: str) -> str:
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"


def tool_current_time() -> str:
    return datetime.now().strftime("%A, %d %B %Y, %H:%M")


def tool_search_documents(query: str) -> str:
    hits = retrieve(query, k=3)
    if not hits:
        return "No documents indexed or nothing relevant found."
    return "\n---\n".join(f"({h['source']}) {h['text']}" for h, _ in hits)


TOOL_FUNCS = {
    "calculator": tool_calculator,
    "current_time": tool_current_time,
    "search_documents": tool_search_documents,
}
TOOLS = [
    {"type": "function", "function": {
        "name": "calculator", "description": "Evaluate a math expression like '12*(3+4)'.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "current_time", "description": "Get the current date and time.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "search_documents",
        "description": "Search the user's uploaded documents (build index in the RAG lab first).",
        "parameters": {"type": "object",
                       "properties": {"query": {"type": "string"}},
                       "required": ["query"]}}},
]


def agent_page():
    st.header("🤖 Agent")
    st.write("The model decides **which tool to call**, reads the result, and continues until done. "
             "Try: *What is 15% of 2480, and what day is it today?*")
    task = st.text_input("Give the agent a task")
    if not task:
        return

    messages = [
        {"role": "system", "content": "You are a helpful agent. Use tools when they help. "
                                      "Think step by step and give a short final answer."},
        {"role": "user", "content": task},
    ]
    max_steps = 5
    for step in range(max_steps):
        resp = client.chat.completions.create(
            model=model, temperature=0, messages=messages, tools=TOOLS, tool_choice="auto"
        )
        msg = resp.choices[0].message
        if not msg.tool_calls:
            st.success("Final answer")
            st.markdown(msg.content)
            return
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [{"id": t.id, "type": "function",
                            "function": {"name": t.function.name, "arguments": t.function.arguments}}
                           for t in msg.tool_calls],
        })
        for t in msg.tool_calls:
            args = json.loads(t.function.arguments or "{}")
            result = TOOL_FUNCS[t.function.name](**args)
            with st.expander(f"Step {step+1}: {t.function.name}({args})", expanded=True):
                st.code(result)
            messages.append({"role": "tool", "tool_call_id": t.id, "content": result})
    st.error("Agent stopped after 5 steps (a safety limit). Try a simpler task.")


# ---------------------------------------------------------------------- router
if page.startswith("💬"):
    chatbot_page()
elif page.startswith("📄"):
    rag_page()
else:
    agent_page()
