#!/usr/bin/env python3
import os
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

DOSSIER_DIR = os.path.expanduser("~/M82/dossier")
CHROMA_DIR = os.path.expanduser("~/M82/chroma_db")

os.makedirs(DOSSIER_DIR, exist_ok=True)

# Usamos embeddings ligeros y locales
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="molina82_dossier", embedding_function=emb_fn)

def process_files():
    doc_id = 0
    for file in os.listdir(DOSSIER_DIR):
        path = os.path.join(DOSSIER_DIR, file)
        text = ""
        if file.endswith(".pdf"):
            reader = PdfReader(path)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        
        if text:
            # Dividir en fragmentos de 500 caracteres
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            for chunk in chunks:
                doc_id += 1
                collection.upsert(
                    documents=[chunk],
                    metadatas=[{"source": file}],
                    ids=[f"id_{doc_id}"]
                )
    print(f"[MOLINA82 BRAIN] Procesados {doc_id} fragmentos en ChromaDB.")

if __name__ == "__main__":
    process_files()
