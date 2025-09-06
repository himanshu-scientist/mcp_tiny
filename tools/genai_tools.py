# # tools/genai_tools.py

# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("all-MiniLM-L6-v2")  # Load your model once

# def embed_text(text: str) -> list:
#     """Return the embedding of the input text."""
#     return model.encode(text).tolist()

# def compare_texts(text1: str, text2: str) -> float:
#     """Return cosine similarity between two texts."""
#     from sklearn.metrics.pairwise import cosine_similarity
#     emb1 = model.encode([text1])
#     emb2 = model.encode([text2])
#     return float(cosine_similarity(emb1, emb2)[0][0])


# tools/genai_tools.py

import boto3
import json
from sklearn.metrics.pairwise import cosine_similarity
from fastmcp import FastMCP, Context

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")  # Use your region

MODEL_ID = "amazon.titan-embed-text-v1"




async def embed_text(text: str) -> list:
    #await ctx.info(f"Embedding text: {text}")
    """Return embedding of texts using Titan embeddings."""
    payload = {
        "inputText": text
    }
    try:
        response = bedrock.invoke_model(
            body=json.dumps(payload),
            modelId=MODEL_ID,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response["body"].read())
        embedding = response_body["embedding"]
        #await ctx.debug(f"Embedding length: {len(embedding)}")
        return embedding
    except Exception as e:
        #await ctx.error(f"Error during embedding: {str(e)}")
        raise


async def compare_texts(text1: str, text2: str) -> float:
    """Return cosine similarity between two texts using Titan embeddings."""
    #await ctx.info("Starting comparison", extra={"text1": text1, "text2": text2})
    emb1 = [await embed_text(text1)]
    emb2 = [await embed_text(text2)]
    similarity = float(cosine_similarity(emb1, emb2)[0][0])
    #await ctx.info(f"Cosine similarity: {similarity}")
    return similarity

# if __name__ == "__main__":
#     text_a = "The quick brown fox jumps over the lazy dog."
#     text_b = "A fast dark-colored fox leaps above a sleepy canine."
#     similarity = compare_texts(text_a, text_b)
#     print(f"Cosine Similarity: {similarity}")
#     print(f"Embedding for text A: {embed_text(text_a)}")


