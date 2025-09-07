import boto3
import json
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")  # Use your region

MODEL_ID = "amazon.titan-embed-text-v1"

def embed_text(text: str) -> list:
    """Return the embedding of the input text using Amazon Titan."""
    payload = {
        "inputText": text
    }
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]

def compare_texts(text1: str, text2: str) -> float:
    """Return cosine similarity between two texts using Titan embeddings."""
    emb1 = [embed_text(text1)]
    emb2 = [embed_text(text2)]
    return float(cosine_similarity(emb1, emb2)[0][0])

# if __name__ == "__main__":
#     text_a = "The quick brown fox jumps over the lazy dog."
#     text_b = "A fast dark-colored fox leaps above a sleepy canine."
#     similarity = compare_texts(text_a, text_b)
#     print(f"Cosine Similarity: {similarity}")
#     print(f"Embedding for text A: {embed_text(text_a)}")