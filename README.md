# DocuBot — PDF Question Answering System

An AI-powered RAG (Retrieval Augmented Generation) system that lets you upload any PDF and ask questions about it in natural language.

## How it works

1. PDF is loaded and split into chunks
2. Chunks are converted to vectors using SentenceTransformer
3. Vectors are stored in ChromaDB (vector database)
4. User question is converted to vector
5. ChromaDB finds most relevant chunks
6. LLaMA3 (via Groq) answers using those chunks

## Tech Stack

- **LLM** — LLaMA3 via Groq API
- **Vector DB** — ChromaDB
- **Embeddings** — SentenceTransformer (all-MiniLM-L6-v2)
- **PDF parsing** — PyPDF

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/docubot.git
cd docubot
```

2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add your API key

```bash
cp .env.example .env
# Open .env and add your Groq API key
# Get free key at console.groq.com
```

5. Run the app

```bash
python app.py
```

## Usage

- Place your PDF inside the `uploads/` folder
- Run `python app.py`
- Enter the PDF filename when prompted
- Ask any question about the PDF!

## Architecture

```
docubot/
  app.py          → Main interface
  rag.py          → RAG pipeline logic
  uploads/        → Place PDFs here
  .env            → API keys (never commit!)
  requirements.txt
```

## Assumptions

- One PDF loaded per session
- Top 3 most relevant chunks sent to LLM
- SQLite used by ChromaDB for local storage
