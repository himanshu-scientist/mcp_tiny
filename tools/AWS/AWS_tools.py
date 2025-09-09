# # tools/genai/genai_tools.py

# import boto3
# import json
# from sklearn.metrics.pairwise import cosine_similarity

# # Initialize Bedrock client
# bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")  # Use your region

# MODEL_ID = "amazon.titan-embed-text-v1"



# class AWSTool:
#     def embed_text(self, text: str) -> list:
#         #await ctx.info(f"Embedding text: {text}")
#         """Return embedding of texts using Titan embeddings."""
#         payload = {
#             "inputText": text
#         }
#         try:
#             response = bedrock.invoke_model(
#                 body=json.dumps(payload),
#                 modelId=MODEL_ID,
#                 accept="application/json",
#                 contentType="application/json"
#             )
#             response_body = json.loads(response["body"].read())
#             embedding = response_body["embedding"]
            
#             return embedding
#         except Exception as e:
#             raise
    

# genai_tool = AWSTool()

# def embed_text(text):
    
#     """Return embedding of texts using Titan embeddings."""
#     return genai_tool.embed_text(text)




