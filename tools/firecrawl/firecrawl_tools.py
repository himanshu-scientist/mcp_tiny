# tools/genai/genai_tools.py

# import boto3
# import json



# class FireCrawlTool:
#     def embed_text(self, text: str) -> list:
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
    

# genai_tool = FireCrawlTool()

# def embed_text(text):
    
#     """Return embedding of texts using Titan embeddings."""
#     return genai_tool.embed_text(text)

# def compare_texts(text1, text2):
#     """Return cosine similarity between two texts using Titan embeddings."""
#     return genai_tool.compare_texts(text1, text2)


