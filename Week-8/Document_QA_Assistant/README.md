# Intelligent Document Q&A Assistant

A RAG-based application that lets users upload PDF documents and ask natural-language questions. The system extracts page-level text, splits it into chunks, stores embeddings in ChromaDB, retrieves relevant passages, and uses Google Gemini to generate answers grounded in the uploaded documents.

## Features

- PDF upload and validation
- Page-level text extraction with PyMuPDF
- Recursive text chunking with overlap
- Local Sentence Transformer embeddings
- Persistent ChromaDB vector store
- Semantic retrieval with relevance filtering
- Gemini-powered RAG answers
- Page and document source references
- Multiple-document knowledge base
- Duplicate upload protection
- Individual document deletion
- Conversation history and follow-up questions
- Streamlit frontend
- FastAPI backend with Swagger UI
- Health endpoint and logging

## Architecture

```text
Streamlit
   |
   v
FastAPI
   |
   +--> Upload --> PyMuPDF --> Chunking --> ChromaDB
   |
   +--> Chat --> ChromaDB retrieval --> Gemini --> Answer + Sources
   |
   +--> Documents --> List/Delete
```

## Setup

Use Python 3.12 in the existing internship environment.

```powershell
cd Document_QA_Assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your Gemini API key:

```env
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
```

## Rebuild the vector database

Put PDFs inside `uploads/`, then run:

```powershell
python rebuild_db.py
```

The script clears the current Chroma collection and indexes every PDF in `uploads/`.

## Run the backend

```powershell
python -m uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Health:

```text
http://127.0.0.1:8000/health
```

## Run the frontend

Open a second terminal in the project folder:

```powershell
streamlit run frontend/app.py
```

## Test flow

1. Start FastAPI.
2. Start Streamlit.
3. Upload a PDF.
4. Confirm it appears in the document list.
5. Ask a question whose answer is clearly present in the PDF.
6. Check the answer and page/document sources.
7. Ask a follow-up question using words such as "it" or "this".
8. Upload a second PDF and test retrieval across documents.
9. Delete one PDF and confirm its embeddings are removed.

## Notes

The current PDF extractor handles text-based PDFs. Scanned/image-only PDFs require OCR before their text can be indexed.

Never commit `.env`, API keys, uploaded PDFs, logs, or the local Chroma database.
