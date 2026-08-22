# 📄 Intelligent Document Q&A Assistant

An AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**, **Google Gemini**, **Sentence Transformers**, **ChromaDB**, **FastAPI**, and **Streamlit**.

The application allows users to upload multiple PDF documents, ask natural-language questions, receive document-grounded answers, view source/page references, maintain conversation history, and listen to answers using multilingual text-to-speech.

---

## 🚀 Features

- 📄 Multiple PDF upload
- 🔎 Semantic document search
- 🤖 Gemini-powered question answering
- 🧠 Retrieval-Augmented Generation (RAG)
- 📚 Document-wise question answering
- 📑 Source and page references
- 💬 Conversation history
- 🔄 Follow-up questions
- 🔊 Text-to-Speech
- 🌐 English, Hindi and Marathi voice support
- 🗑️ Document deletion
- ⚡ FastAPI backend
- 🎨 Streamlit frontend
- 🗃️ ChromaDB vector database
- 📝 Logging and error handling

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ├── PDF Upload
 │      │
 │      ▼
 │   Text Extraction
 │      │
 │      ▼
 │   Text Chunking
 │      │
 │      ▼
 │   Embeddings
 │      │
 │      ▼
 │   ChromaDB
 │
 └── User Question
        │
        ▼
   Semantic Search
        │
        ▼
   Relevant Chunks
        │
        ▼
   Gemini LLM
        │
        ▼
   Final Answer
        │
        ├── Sources
        │
        └── Text-to-Speech