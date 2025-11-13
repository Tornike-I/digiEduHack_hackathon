import re
from typing import List, Dict
from . import retrieval_logic  # for token functions
from ..db.vector_store import VectorStore

# simple chunker: split by sentences and group to approx chunk_size words
def chunk_text(text: str, chunk_size_words: int = 200, overlap: int = 20) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    n = len(words)
    while i < n:
        chunk = " ".join(words[i:i + chunk_size_words])
        chunks.append(chunk)
        i += chunk_size_words - overlap
    return chunks

def tokenize(text: str) -> Dict[str,int]:
    # reuse retrieval logic's tokenizer for consistent tokens
    return retrieval_logic.token_counts(text)

def ingest_document(text: str, metadata: dict = None) -> dict:
    chunks = chunk_text(text)
    tokens_list = [tokenize(c) for c in chunks]
    store = VectorStore()
    store.insert_chunks(chunks, tokens_list, metadata=metadata)
    return {"inserted_chunks": len(chunks)}
