import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Intelligent Document Q&A Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .title { font-size: 2.3rem; font-weight: 750; margin-bottom: 0.1rem; }
    .subtitle { color: #777; margin-bottom: 1.5rem; }
    .source-card { padding: 10px 14px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 7px; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def backend_online():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.ok
    except requests.RequestException:
        return False


def get_documents():
    try:
        response = requests.get(f"{API_URL}/documents/", timeout=10)
        if response.ok:
            return response.json().get("documents", [])
    except requests.RequestException:
        pass
    return []


def upload_pdf(uploaded_file):
    try:
        return requests.post(
            f"{API_URL}/upload/",
            files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
            timeout=180,
        )
    except requests.RequestException as exc:
        st.error(f"Backend connection failed: {exc}")
        return None


def delete_pdf(filename):
    try:
        return requests.delete(f"{API_URL}/documents/{filename}", timeout=20)
    except requests.RequestException as exc:
        st.error(f"Backend connection failed: {exc}")
        return None


def ask_question(question, history):
    try:
        return requests.post(
            f"{API_URL}/chat/",
            json={"question": question, "history": history},
            timeout=180,
        )
    except requests.RequestException as exc:
        st.error(f"Backend connection failed: {exc}")
        return None


def show_sources(sources):
    if not sources:
        return
    st.markdown("**📚 Sources**")
    seen = set()
    for source in sources:
        document = source.get("document", "Unknown")
        page = source.get("page", "Unknown")
        key = (document, page)
        if key in seen:
            continue
        seen.add(key)
        st.markdown(
            f'<div class="source-card">📄 <b>{document}</b><br>📖 Page: {page}</div>',
            unsafe_allow_html=True,
        )


with st.sidebar:
    st.title("📄 Document Assistant")

    if backend_online():
        st.success("🟢 Backend Connected")
    else:
        st.error("🔴 Backend Offline")
        st.code("python -m uvicorn app.main:app --reload")

    st.divider()
    st.subheader("📤 Upload PDF")
    uploaded = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded and st.button("🚀 Upload & Index", use_container_width=True):
        if not backend_online():
            st.error("Start the FastAPI backend first.")
        else:
            with st.spinner("Extracting, chunking and indexing..."):
                response = upload_pdf(uploaded)
            if response is not None:
                if response.ok:
                    data = response.json()
                    st.success(data["message"])
                    st.caption(f"Pages: {data['pages']} | Chunks: {data['chunks']}")
                    st.rerun()
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(detail)

    st.divider()
    st.subheader("📚 Documents")
    documents = get_documents()

    if documents:
        st.caption(f"{len(documents)} document(s)")
        for document in documents:
            st.markdown(f"📄 **{document}**")
            if st.button("🗑️ Delete", key=f"delete_{document}", use_container_width=True):
                with st.spinner("Deleting..."):
                    response = delete_pdf(document)
                if response is not None and response.ok:
                    st.success("Deleted")
                    st.rerun()
                elif response is not None:
                    try:
                        st.error(response.json().get("detail", response.text))
                    except Exception:
                        st.error(response.text)
    else:
        st.info("No PDFs uploaded yet.")

    st.divider()
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


st.markdown('<div class="title">🤖 Intelligent Document Q&A Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Ask questions from your uploaded PDFs using Retrieval-Augmented Generation.</div>',
    unsafe_allow_html=True,
)

if documents:
    st.info(f"📚 Knowledge base: **{len(documents)} document(s)**")
else:
    st.warning("Upload a PDF from the sidebar to start asking questions.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            show_sources(message.get("sources", []))

if not st.session_state.messages:
    st.markdown("### 💬 Try asking")
    c1, c2, c3 = st.columns(3)
    c1.info("**What is an Operating System?**")
    c2.info("**What are the functions of an OS?**")
    c3.info("**Explain process management.**")

question = st.chat_input("Ask a question about your documents...")

if question:
    history = [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.messages
    ]

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not backend_online():
            answer = "⚠️ **Backend is not running.** Start FastAPI first."
            sources = []
            st.error(answer)
        elif not documents:
            answer = "📂 **No documents are uploaded yet.** Upload a PDF first."
            sources = []
            st.warning(answer)
        else:
            with st.spinner("🔎 Searching documents and generating answer..."):
                response = ask_question(question, history)

            if response is not None and response.ok:
                data = response.json()
                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])
                st.markdown(answer)
                show_sources(sources)
            else:
                if response is None:
                    detail = "Unable to connect to backend."
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                answer = f"⚠️ **Backend Error**\n\n{detail}"
                sources = []
                st.error(detail)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
