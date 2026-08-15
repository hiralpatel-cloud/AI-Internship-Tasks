import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Intelligent Document Q&A Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .title {
        font-size: 2.3rem;
        font-weight: 750;
        margin-bottom: 0.1rem;
    }

    .subtitle {
        color: #777;
        margin-bottom: 1.5rem;
    }

    .source-card {
        padding: 10px 14px;
        border: 1px solid #ddd;
        border-radius: 10px;
        margin-bottom: 7px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# BACKEND FUNCTIONS
# ============================================================

def backend_online():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        return response.ok

    except requests.RequestException:
        return False


def get_documents():
    try:
        response = requests.get(
            f"{API_URL}/documents/",
            timeout=10
        )

        if response.ok:
            return response.json().get(
                "documents",
                []
            )

    except requests.RequestException:
        pass

    return []


def upload_pdf(uploaded_file):
    try:
        return requests.post(
            f"{API_URL}/upload/",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            },
            timeout=180,
        )

    except requests.RequestException as exc:
        st.error(
            f"Backend connection failed: {exc}"
        )
        return None


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


def ask_question(question, history):
    try:
        return requests.post(
            f"{API_URL}/chat/",
            json={
                "question": question,
                "history": history
            },
            timeout=180,
        )

    except requests.RequestException as exc:
        st.error(
            f"Backend connection failed: {exc}"
        )
        return None


# ============================================================
# TEXT TO SPEECH FUNCTION
# ============================================================

def generate_audio(text, language):
    try:
        return requests.post(
            f"{API_URL}/tts/generate",
            json={
                "text": text,
                "language": language,
            },
            timeout=180,
        )

    except requests.RequestException as exc:
        st.error(
            f"Audio generation failed: {exc}"
        )
        return None


# ============================================================
# SOURCE DISPLAY
# ============================================================

def show_sources(sources):

    if not sources:
        return

    st.markdown("**📚 Sources**")

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
            f"""
            <div class="source-card">
                📄 <b>{document}</b><br>
                📖 Page: {page}
            </div>
            """,
            unsafe_allow_html=True,
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
    # PDF UPLOAD
    # --------------------------------------------------------

    st.subheader("📤 Upload PDF")

    uploaded = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded and st.button(
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

                response = upload_pdf(uploaded)

            if response is not None:

                if response.ok:

                    data = response.json()

                    st.success(
                        data["message"]
                    )

                    st.caption(
                        f"Pages: {data['pages']} | "
                        f"Chunks: {data['chunks']}"
                    )

                    st.rerun()

                else:

                    try:

                        detail = response.json().get(
                            "detail",
                            response.text
                        )

                    except Exception:

                        detail = response.text

                    st.error(detail)

    st.divider()

    # --------------------------------------------------------
    # DOCUMENT LIST
    # --------------------------------------------------------

    st.subheader("📚 Documents")

    documents = get_documents()

    if documents:

        st.caption(
            f"{len(documents)} document(s)"
        )

        for document in documents:

            st.markdown(
                f"📄 **{document}**"
            )

            if st.button(
                "🗑️ Delete",
                key=f"delete_{document}",
                use_container_width=True
            ):

                with st.spinner(
                    "Deleting..."
                ):

                    response = delete_pdf(
                        document
                    )

                if response is not None and response.ok:

                    st.success(
                        "Deleted"
                    )

                    st.rerun()

                elif response is not None:

                    try:

                        st.error(
                            response.json().get(
                                "detail",
                                response.text
                            )
                        )

                    except Exception:

                        st.error(
                            response.text
                        )

    else:

        st.info(
            "No PDFs uploaded yet."
        )

    st.divider()

    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.button(
        "🧹 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# MAIN PAGE HEADER
# ============================================================

st.markdown(
    '<div class="title">'
    '🤖 Intelligent Document Q&A Assistant'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions from your uploaded PDFs using '
    'Retrieval-Augmented Generation.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# KNOWLEDGE BASE STATUS
# ============================================================

if documents:

    st.info(
        f"📚 Knowledge base: "
        f"**{len(documents)} document(s)**"
    )

else:

    st.warning(
        "Upload a PDF from the sidebar "
        "to start asking questions."
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # ----------------------------------------------------
        # ASSISTANT MESSAGE
        # ----------------------------------------------------

        if message["role"] == "assistant":

            # Show sources
            show_sources(
                message.get(
                    "sources",
                    []
                )
            )

            # Show previously generated audio
            audio_files = message.get(
                "audio_files",
                []
            )

            if audio_files:

                st.markdown(
                    "**🔊 Listen to Answer**"
                )

                for audio_file in audio_files:

                    audio_path = (
                        f"{API_URL}/tts/audio/"
                        f"{audio_file}"
                    )

                    try:

                        audio_response = requests.get(
                            audio_path,
                            timeout=30
                        )

                        if audio_response.ok:

                            st.audio(
                                audio_response.content,
                                format="audio/mp3"
                            )

                    except requests.RequestException:

                        st.warning(
                            "Unable to load audio."
                        )


# ============================================================
# EMPTY CHAT MESSAGE
# ============================================================

if not st.session_state.messages:

    st.markdown(
        "### 💬 Try asking"
    )

    c1, c2, c3 = st.columns(3)

    c1.info(
        "**What is an Operating System?**"
    )

    c2.info(
        "**What are the functions of an OS?**"
    )

    c3.info(
        "**Explain process management.**"
    )


# ============================================================
# VOICE LANGUAGE
# ============================================================

st.markdown(
    "### 🌐 Voice Language"
)

selected_language = st.selectbox(
    "Choose the language for audio:",
    options=[
        "English",
        "Hindi",
        "Marathi"
    ],
    index=0,
)


# Language codes used by gTTS/backend

LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
}


language_code = LANGUAGE_CODES[
    selected_language
]


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about your documents..."
)


# ============================================================
# QUESTION PROCESSING
# ============================================================

if question:

    # --------------------------------------------------------
    # CHAT HISTORY FOR RAG
    # --------------------------------------------------------

    history = [
        {
            "role": message["role"],
            "content": message["content"]
        }

        for message in st.session_state.messages
    ]


    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            question
        )


    # --------------------------------------------------------
    # INITIALIZE VARIABLES
    # --------------------------------------------------------

    answer = ""

    sources = []

    audio_files = []


    # --------------------------------------------------------
    # ASSISTANT RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        # ====================================================
        # CHECK BACKEND
        # ====================================================

        if not backend_online():

            answer = (
                "⚠️ **Backend is not running.** "
                "Start FastAPI first."
            )

            sources = []

            st.error(
                answer
            )


        # ====================================================
        # CHECK DOCUMENTS
        # ====================================================

        elif not documents:

            answer = (
                "📂 **No documents are uploaded yet.** "
                "Upload a PDF first."
            )

            sources = []

            st.warning(
                answer
            )


        # ====================================================
        # ASK RAG QUESTION
        # ====================================================

        else:

            with st.spinner(
                "🔎 Searching documents "
                "and generating answer..."
            ):

                response = ask_question(
                    question,
                    history
                )


            # =================================================
            # SUCCESSFUL RAG RESPONSE
            # =================================================

            if response is not None and response.ok:

                data = response.json()


                # ---------------------------------------------
                # GET ANSWER
                # ---------------------------------------------

                answer = data.get(
                    "answer",
                    "No answer returned."
                )


                # ---------------------------------------------
                # GET SOURCES
                # ---------------------------------------------

                sources = data.get(
                    "sources",
                    []
                )


                # ---------------------------------------------
                # DISPLAY ANSWER
                # ---------------------------------------------

                st.markdown(
                    answer
                )


                # ---------------------------------------------
                # DISPLAY SOURCES
                # ---------------------------------------------

                show_sources(
                    sources
                )


                # =================================================
                # TEXT TO SPEECH
                # =================================================

                st.markdown(
                    "### 🔊 Listen to Answer"
                )


                with st.spinner(
                    f"Generating "
                    f"{selected_language} audio..."
                ):

                    audio_response = generate_audio(
                        answer,
                        language_code
                    )


                # =================================================
                # TTS SUCCESS
                # =================================================

                if (
                    audio_response is not None
                    and audio_response.ok
                ):

                    audio_data = (
                        audio_response.json()
                    )


                    audio_files = (
                        audio_data.get(
                            "files",
                            []
                        )
                    )


                    if audio_files:

                        st.success(
                            f"🔊 "
                            f"{selected_language} "
                            f"audio generated!"
                        )


                        # -----------------------------------------
                        # PLAY AUDIO
                        # -----------------------------------------

                        for audio_file in audio_files:

                            audio_url = (
                                f"{API_URL}/tts/audio/"
                                f"{audio_file}"
                            )


                            try:

                                file_response = (
                                    requests.get(
                                        audio_url,
                                        timeout=30
                                    )
                                )


                                if file_response.ok:

                                    st.audio(
                                        file_response.content,
                                        format="audio/mp3"
                                    )


                                else:

                                    st.warning(
                                        "Unable to load "
                                        "generated audio."
                                    )


                            except requests.RequestException:

                                st.warning(
                                    "Unable to load "
                                    "generated audio."
                                )


                    else:

                        st.warning(
                            "TTS service returned "
                            "no audio files."
                        )


                # =================================================
                # TTS ERROR
                # =================================================

                else:

                    if audio_response is not None:

                        try:

                            detail = (
                                audio_response.json().get(
                                    "detail",
                                    audio_response.text
                                )
                            )

                        except Exception:

                            detail = (
                                audio_response.text
                            )


                        st.warning(
                            f"Audio generation failed: "
                            f"{detail}"
                        )


            # =================================================
            # RAG BACKEND ERROR
            # =================================================

            else:

                if response is None:

                    detail = (
                        "Unable to connect to backend."
                    )

                else:

                    try:

                        detail = (
                            response.json().get(
                                "detail",
                                response.text
                            )
                        )

                    except Exception:

                        detail = response.text


                answer = (
                    f"⚠️ **Backend Error**\n\n"
                    f"{detail}"
                )

                sources = []

                st.error(
                    detail
                )


    # ========================================================
    # SAVE ASSISTANT RESPONSE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "audio_files": audio_files,
            "language": selected_language,
        }
    )