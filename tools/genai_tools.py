# tools/genai_tools.py

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # Load your model once

def embed_text(text: str) -> list:
    """Return the embedding of the input text."""
    return model.encode(text).tolist()

def compare_texts(text1: str, text2: str) -> float:
    """Return cosine similarity between two texts."""
    from sklearn.metrics.pairwise import cosine_similarity
    emb1 = model.encode([text1])
    emb2 = model.encode([text2])
    return float(cosine_similarity(emb1, emb2)[0][0])
