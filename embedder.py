# import os
# # import openai
# import requests
# from dotenv import load_dotenv

# load_dotenv()
# # openai.api_key = os.getenv("OPENAI_API_KEY")

# # EMBED_MODEL = "text-embedding-ada-002"

# QWEN_EMBED_API_URL = "http://optimus-ai.smartester.io:20005/api/embeddings"  # <-- Update to actual Qwen embedding endpoint
# QWEN_API_KEY = "b57be2e475c44228ba79390a4f0bb6aab1aa2c7986a2dbea066f96c8a316c7a5"


# def embed_texts(texts: list) -> list:
#     """
#     Embeds a list of texts using Qwen's embedding API.
#     Returns a list of embedding vectors (lists of floats).
#     """
#     headers = {
#         "Authorization": f"Bearer {QWEN_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "qwen-embedding-model",  # <-- Update to actual Qwen embedding model name
#         "input": texts
#     }
#     response = requests.post(QWEN_EMBED_API_URL, headers=headers, json=data)
#     response.raise_for_status()
#     result = response.json()
#     # Adjust this if the response structure is different
#     return result.get("embeddings", [])

# def embed_text(text: str) -> list:
#     """
#     Embeds a single text string.
#     """
#     return embed_texts([text])[0]

# # def embed_texts(texts: list) -> list:
# #     """
# #     Embeds a list of texts using OpenAI's text-embedding-ada-002 model.
# #     Returns a list of embedding vectors (lists of floats).
# #     """
# #     response = openai.embeddings.create(
# #         input=texts,
# #         model=EMBED_MODEL
# #     )
# #     return [d.embedding for d in response.data]
# #
# # def embed_text(text: str) -> list:
# #     """
# #     Embeds a single text string.
# #     """
# #     return embed_texts([text])[0]

from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

# Load the embedding model — you can choose a different model if needed
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(EMBED_MODEL)

def embed_texts(texts: list) -> list:
    """
    Embeds a list of texts using a local Hugging Face SentenceTransformer model.
    Returns a list of embedding vectors (lists of floats).
    """
    return model.encode(texts, convert_to_numpy=True).tolist()

def embed_text(text: str) -> list:
    """
    Embeds a single text string.
    """
    return embed_texts([text])[0]