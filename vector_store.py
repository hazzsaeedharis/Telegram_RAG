import os
import redis
import numpy as np
import pickle
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Connect to Redis
r = redis.Redis.from_url(REDIS_URL)

def store_embeddings(chunks: list, embeddings: list):
    """
    Stores each chunk and its embedding in Redis.
    Each entry is stored as a hash: {text, embedding (pickled)}
    Key: "chunk:{i}"
    """
    pipe = r.pipeline()
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        key = f"chunk:{i}"
        pipe.hset(key, mapping={
            "text": chunk,
            "embedding": pickle.dumps(emb)
        })
    pipe.execute()

def get_all_chunks_and_embeddings():
    """
    Retrieves all chunks and their embeddings from Redis.
    Returns a list of (text, embedding) tuples.
    """
    keys = r.keys("chunk:*")
    results = []
    for key in keys:
        data = r.hgetall(key)
        text = data[b"text"].decode("utf-8")
        emb = pickle.loads(data[b"embedding"])
        results.append((text, emb))
    return results

def query_top_k(query_embedding, k=3):
    """
    Finds the top k most similar chunks to the query_embedding using cosine similarity.
    Returns a list of (text, score) tuples.
    """
    all_chunks = get_all_chunks_and_embeddings()
    if not all_chunks:
        return []
    scores = []
    query_vec = np.array(query_embedding)
    for text, emb in all_chunks:
        emb_vec = np.array(emb)
        # Cosine similarity
        sim = np.dot(query_vec, emb_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(emb_vec) + 1e-8)
        scores.append((text, sim))
    # Sort by similarity descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:k]

def clear_all_chunks():
    """
    Deletes all chunk:* keys from Redis.
    """
    keys = r.keys("chunk:*")
    if keys:
        r.delete(*keys)
