import json
from pathlib import Path

import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

HISTORY_FILE = Path(__file__).parent / "chat_history.json"


st.set_page_config(
    page_title="Intelligent Document Q&A Assistant",
    page_icon="📄",
    layout="wide",
)


# ============================================================
# CHAT HISTORY FUNCTIONS
# ============================================================

def load_chat_history():
    """
    Load chat history from chat_history.json.
    """

    if not HISTORY_FILE.exists():
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

    except Exception:
        pass

    return []


def save_chat_history(messages):
    """
    Save chat history to chat_history.json.
    """

    try:

        clean_messages = []

        for message in messages:

            clean_message = {
                "role": message.get("role", ""),
                "content": message.get("content", ""),
                "sources": message.get("sources", []),
            }

            # Do NOT store audio bytes in JSON
            clean_messages.append(clean_message)

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                clean_messages,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as exc:

        st.warning(
            f"Could not save chat history: {exc}"
        )


def clear_chat_history():

    try:

        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()

    except Exception:
        pass

    st.session_state.messages = []


# ============================================================
# INITIALIZE SESSION
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = load_chat_history()


# ============================================================
# BACKEND CONNECTION
# ============================================================

def backend_online():

    try:

        response = requests.get(
            f"{API_URL}/health/",
            timeout=5
        )

        return response.ok

    except requests.RequestException:

        return False


# ============================================================
# GET DOCUMENTS
# ============================================================

def get_documents():

    try:

        response = requests.get(
            f"{API_URL}/documents/",
            timeout=10
        )

        if response.ok:

            data = response.json()

            return data.get(
                "documents",
                []
            )

    except requests.RequestException:
        pass

    return []


# ============================================================
# UPLOAD PDFs
# ============================================================

def upload_pdfs(uploaded_files):

    try:

        files = [
            (
                "files",
                (
                    file.name,
                    file.getvalue(),
                    "application/pdf"
                )
            )

            for file in uploaded_files
        ]

        return requests.post(
            f"{API_URL}/upload/",
            files=files,
            timeout=300
        )

    except requests.RequestException as exc:

        st.error(
            f"Backend connection failed: {exc}"
        )

        return None


# ============================================================
# DELETE PDF
# ============================================================

def delete_pdf(filename):

    try:

        return requests.delete(
            f"{API_URL}/documents/{filename}",
            timeout=20
        )

    except requests.RequestException as exc:

        st.error(
            f"Backend connection failed: {exc}"
        )

        return None


# ============================================================
# ASK QUESTION
# ============================================================

def ask_question(
    question,
    document
):

    # Send previous conversation
    # to the backend for context.

    history = []

    for message in st.session_state.messages:

        history.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    try:

        return requests.post(

            f"{API_URL}/chat/",

            json={
                "question": question,

                "history": history,

                "document": document,
            },

            timeout=180,
        )

    except requests.RequestException as exc:

        st.error(
            f"Backend connection failed: {exc}"
        )

        return None


# ============================================================
# GENERATE AUDIO
# ============================================================

def generate_audio(
    text,
    language
):

    try:

        return requests.post(

            f"{API_URL}/tts/generate",

            json={
                "text": text,
                "language": language
            },

            timeout=180,
        )

    except requests.RequestException as exc:

        st.warning(
            f"Audio generation failed: {exc}"
        )

        return None


# ============================================================
# SHOW SOURCES
# ============================================================

def show_sources(sources):

    if not sources:
        return

    with st.expander("📚 Sources"):

        seen = set()

        for source in sources:

            document = source.get(
                "document",
                "Unknown"
            )

            page = source.get(
                "page",
                "Unknown"
            )

            key = (
                document,
                page
            )

            if key in seen:
                continue

            seen.add(key)

            st.markdown(
                f"📄 **{document}** — "
                f"Page **{page}**"
            )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📄 Document Assistant")

    # --------------------------------------------------------
    # BACKEND STATUS
    # --------------------------------------------------------

    if backend_online():

        st.success(
            "🟢 Backend Connected"
        )

    else:

        st.error(
            "🔴 Backend Offline"
        )

        st.code(
            "python -m uvicorn app.main:app --reload"
        )

    st.divider()

    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    st.subheader(
        "📤 Upload PDFs"
    )

    uploaded_files = st.file_uploader(

        "Choose one or more PDF files",

        type=["pdf"],

        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button(
            "🚀 Upload & Index",
            use_container_width=True
        ):

            if not backend_online():

                st.error(
                    "Start the FastAPI backend first."
                )

            else:

                with st.spinner(
                    "Extracting, chunking and indexing..."
                ):

                    response = upload_pdfs(
                        uploaded_files
                    )

                if response is not None:

                    try:

                        data = response.json()

                    except Exception:

                        data = {
                            "detail": response.text
                        }

                    if response.ok:

                        st.success(
                            data.get(
                                "message",
                                "Upload complete."
                            )
                        )

                        for item in data.get(
                            "results",
                            []
                        ):

                            if item.get(
                                "status"
                            ) == "indexed":

                                st.caption(
                                    f"📄 {item.get('filename')} | "
                                    f"{item.get('pages')} pages | "
                                    f"{item.get('chunks')} chunks"
                                )

                            else:

                                st.warning(
                                    f"{item.get('filename')}: "
                                    f"{item.get('error')}"
                                )

                        st.rerun()

                    else:

                        st.error(
                            data.get(
                                "detail",
                                response.text
                            )
                        )

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    st.divider()

    documents = get_documents()

    st.subheader(
        f"📚 Documents ({len(documents)})"
    )

    if documents:

        for document in documents:

            st.markdown(
                f"📄 **{document}**"
            )

            if st.button(
                "🗑️ Delete",
                key=f"delete_{document}",
                use_container_width=True
            ):

                response = delete_pdf(
                    document
                )

                if (
                    response is not None
                    and response.ok
                ):

                    st.success(
                        "Deleted."
                    )

                    st.rerun()

                elif response is not None:

                    st.error(
                        response.text
                    )

    else:

        st.info(
            "No PDFs indexed yet."
        )

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "💬 Chat History"
    )

    if st.session_state.messages:

        st.success(
            f"{len(st.session_state.messages)} "
            "messages stored"
        )

    else:

        st.info(
            "No chat messages yet."
        )

    if st.button(
        "🧹 Clear Chat History",
        use_container_width=True
    ):

        clear_chat_history()

        st.success(
            "Chat history cleared."
        )

        st.rerun()


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "🤖 Intelligent Document Q&A Assistant"
)

st.caption(
    "Multi-document RAG with document filtering, "
    "conversation history and multilingual voice."
)


# ============================================================
# DOCUMENT STATUS
# ============================================================

documents = get_documents()

if documents:

    st.info(
        f"Knowledge base: **{len(documents)} document(s)**"
    )

else:

    st.warning(
        "Upload at least one PDF from the sidebar."
    )


# ============================================================
# DOCUMENT SELECTION
# ============================================================

selected = st.selectbox(

    "📚 Question Scope",

    ["All Documents"] + documents
)


if selected == "All Documents":

    selected_document = None

else:

    selected_document = selected


# ============================================================
# LANGUAGE
# ============================================================

language = st.selectbox(

    "🔊 Answer language",

    [
        "English",
        "Hindi",
        "Marathi"
    ]
)


language_code = {

    "English": "english",

    "Hindi": "hindi",

    "Marathi": "marathi"

}[language]


# ============================================================
# DISPLAY EXISTING CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message["role"] == "assistant":

            show_sources(
                message.get(
                    "sources",
                    []
                )
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(

    "Ask a question about your uploaded PDF(s)..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    question = question.strip()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not question:

        st.error(
            "Question cannot be empty."
        )

        st.stop()


    if not documents:

        st.error(
            "Please upload a PDF first."
        )

        st.stop()


    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    user_message = {

        "role": "user",

        "content": question,

        "sources": []
    }


    st.session_state.messages.append(
        user_message
    )


    # SAVE IMMEDIATELY

    save_chat_history(
        st.session_state.messages
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            response = ask_question(

                question,

                selected_document
            )


        if response is None:

            st.stop()


        try:

            data = response.json()

        except Exception:

            data = {
                "detail": response.text
            }


        if not response.ok:

            st.error(
                data.get(
                    "detail",
                    "Request failed."
                )
            )

            st.stop()


        # ----------------------------------------------------
        # ANSWER
        # ----------------------------------------------------

        answer = data.get(
            "answer",
            ""
        )


        sources = data.get(
            "sources",
            []
        )


        if not answer:

            answer = (
                "I couldn't find the answer "
                "in the uploaded documents."
            )


        st.markdown(
            answer
        )


        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        show_sources(
            sources
        )


        # ----------------------------------------------------
        # AUDIO
        # ----------------------------------------------------

        audio_bytes = None


        with st.spinner(
            f"Generating {language} audio..."
        ):

            audio_response = generate_audio(

                answer,

                language_code
            )


        if (
            audio_response is not None
            and audio_response.ok
        ):

            try:

                audio_data = (
                    audio_response.json()
                )

                urls = audio_data.get(
                    "audio_urls",
                    []
                )


                if urls:

                    audio_file_response = requests.get(

                        f"{API_URL}{urls[0]}",

                        timeout=60
                    )


                    if audio_file_response.ok:

                        audio_bytes = (
                            audio_file_response.content
                        )

                        st.audio(
                            audio_bytes,
                            format="audio/mp3"
                        )

            except Exception:

                st.warning(
                    "Audio was generated but "
                    "could not be loaded."
                )


        # ----------------------------------------------------
        # SAVE ASSISTANT MESSAGE
        # ----------------------------------------------------

        assistant_message = {

            "role": "assistant",

            "content": answer,

            "sources": sources
        }


        st.session_state.messages.append(
            assistant_message
        )


        # ----------------------------------------------------
        # SAVE PERMANENTLY
        # ----------------------------------------------------

        save_chat_history(
            st.session_state.messages
        )