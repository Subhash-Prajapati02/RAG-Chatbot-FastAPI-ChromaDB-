# 🤖 RAG Chatbot (FastAPI + ChromaDB)

A lightweight Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions based on their content.

---

## 🚀 Features

* 📄 Upload and process PDF documents
* 🔍 Semantic search using embeddings
* 🧠 Context-aware responses via LLM (Groq)
* ⚡ FastAPI backend with REST endpoints
* 💬 Modern chatbot-style UI

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **LLM:** Groq (Llama 3.1)
* **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **Vector DB:** ChromaDB
* **Frontend:** HTML, CSS, JavaScript

---

## 📁 Project Structure

```
project/
│── main.py
│── rag_pipeline.py
│── .env
│
├── pdf/                # Uploaded PDFs
├── chromadb/           # Vector database storage
├── static/             # CSS & JS files
└── templates/
    └── index.html      # Frontend UI
```

---

## ⚙️ Setup & Installation

1. Clone the repository:

```
git clone <your-repo-url>
cd project
```

2. Create virtual environment:

```
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Add environment variables:

```
API_KEY=your_groq_api_key
```

---

## ▶️ Run the Application

```
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## 📌 API Endpoints

* `GET /` → Load UI
* `POST /upload` → Upload PDF
* `POST /ask` → Ask questions

---

## 🧠 How It Works

1. PDFs are loaded and split into chunks
2. Text is converted into embeddings
3. Stored in ChromaDB
4. Query retrieves relevant chunks
5. LLM generates answer using context

---

## ⚠️ Notes

* Ensure `pdf/` folder exists
* Avoid uploading duplicate files
* Requires valid Groq API key

---

## 📄 License

This project is for educational purposes.
