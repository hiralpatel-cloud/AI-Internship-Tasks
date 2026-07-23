# Week-7: Generative AI, LLMs, Prompt Engineering & Mini RAG

## 📌 Project Overview

This project was developed as part of the AI Internship Week-7 tasks. It covers the fundamentals of Generative AI, Large Language Models (LLMs), Prompt Engineering, AI Chatbots, Embeddings, Vector Databases, Similarity Search, FAISS, and Retrieval-Augmented Generation (RAG).

---

## 🎯 Objectives

- Learn the basics of Generative AI and LLMs.
- Understand Transformers, Tokens, and Embeddings.
- Practice Prompt Engineering techniques.
- Build an AI Chatbot using the Gemini API.
- Learn Similarity Search using FAISS.
- Implement a Mini RAG (Retrieval-Augmented Generation) system.

---

## 🛠 Technologies Used

- Python 3.12
- Google Gemini API
- google-genai
- python-dotenv
- FAISS
- Sentence Transformers
- NumPy
- Visual Studio Code

---

## 📂 Project Structure

```
Week-7/
│── chatbot.py
│── prompt_examples.py
│── faiss_demo.py
│── rag.py
│── knowledge.txt
│── requirements.txt
│── .env
└── README.md
```

---

## 📚 Features

### 🤖 AI Chatbot
- Accepts user input.
- Generates intelligent responses using the Gemini API.
- Runs continuously until the user exits.

### 💡 Prompt Engineering
Demonstrates:
- Zero-shot Prompting
- One-shot Prompting
- Few-shot Prompting
- Chain-of-Thought Prompting

### 🔍 FAISS Similarity Search
- Converts text into embeddings.
- Stores embeddings in a FAISS vector index.
- Retrieves the most relevant documents based on user queries.

### 📖 Mini RAG
- Reads data from a knowledge base.
- Finds relevant information using FAISS.
- Sends the retrieved context to Gemini.
- Generates accurate answers based on the retrieved context.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### 4. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure API Key

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Programs

### AI Chatbot

```bash
python chatbot.py
```

### Prompt Engineering

```bash
python prompt_examples.py
```

### FAISS Similarity Search

```bash
python faiss_demo.py
```

### Mini RAG

```bash
python rag.py
```

---

## 📸 Sample Output

### AI Chatbot

```
You: What is Artificial Intelligence?

Bot:
Artificial Intelligence is the simulation of human intelligence by machines.
```

### FAISS Search

```
Ask a question:
What is RAG?

Top Matches:
1. RAG stands for Retrieval-Augmented Generation.
2. FAISS is a library used for similarity search.
```

---

## 📖 Concepts Covered

- Generative AI
- Large Language Models (LLMs)
- Transformers
- Tokens
- Embeddings
- Prompt Engineering
- Zero-shot Prompting
- One-shot Prompting
- Few-shot Prompting
- Chain-of-Thought Prompting
- Gemini API
- FAISS
- Similarity Search
- Vector Databases
- Retrieval-Augmented Generation (RAG)

---

## 🎯 Learning Outcomes

After completing this project, I learned how to:

- Build an AI chatbot using the Gemini API.
- Design effective prompts for LLMs.
- Generate embeddings from text.
- Store and retrieve embeddings using FAISS.
- Perform semantic similarity search.
- Build a simple Retrieval-Augmented Generation (RAG) application.

---

## 👩‍💻 Author

**Hiral Patel**

AI Internship – Week 7