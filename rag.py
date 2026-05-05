import os
import chromadb
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()

def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def split_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def store_in_chromadb(chunks, collection_name="docubot"):
    try:
        chroma_client.delete_collection(name=collection_name)
    except:
        pass
    collection = chroma_client.get_or_create_collection(
        name=collection_name
    )
    embeddings = embedder.encode(chunks).tolist()
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"chunk_{i}"]
        )
    return collection

def get_relevant_chunks(query, collection, n_results=3):
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results["documents"][0]

def ask_groq(query, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = f"""You are a helpful assistant. Answer the question based only on the context below.
If the answer is not in the context, say 'I could not find this in the document.'

Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def process_pdf_and_answer(pdf_path, query):
    print("Reading PDF...")
    text = load_pdf(pdf_path)
    print("Splitting into chunks...")
    chunks = split_text(text)
    print(f"Storing {len(chunks)} chunks in ChromaDB...")
    collection = store_in_chromadb(chunks)
    print("Finding relevant chunks...")
    relevant_chunks = get_relevant_chunks(query, collection)
    print("Asking Groq (LLaMA3)...")
    answer = ask_groq(query, relevant_chunks)
    return answer