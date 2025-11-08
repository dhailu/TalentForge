# import os
# import requests
# from dotenv import load_dotenv
# load_dotenv()

# # AZ_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/")
# # AZ_KEY = os.getenv("AZURE_OPENAI_API_KEY")
# # EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
# # MAX_LEN = int(os.getenv("AZURE_EMBED_MAX_LENGTH", "2000"))

# # def azure_get_embedding(text):
# #     text = text[:MAX_LEN]
# #     url = f"{AZ_ENDPOINT}/openai/deployments/{EMBED_MODEL}/embeddings?api-version=2024-10-01"
# #     headers = {"api-key": AZ_KEY, "Content-Type": "application/json"}
# #     payload = {"input": text}
# #     r = requests.post(url, headers=headers, json=payload, timeout=30)
# #     r.raise_for_status()
# #     res = r.json()
# #     return res["data"][0]["embedding"]

# # os.path.dirname('updates')

# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is required in .env")    
# import psycopg2
# from psycopg2.extras import execute_values
# import numpy as np
# EMBEDDING_DIM = 1536  # Adjust based on your embedding model
# def get_db_connection():
#     return psycopg2.connect(DATABASE_URL)
# def azure_get_embedding(text):
#     import openai
#     openai.api_type = "azure"
#     openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/")
#     openai.api_version = "2024-10-01"
#     openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
#     EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
#     response = openai.Embedding.create(
#         input=text,
#         engine=EMBED_MODEL
#     )
#     return response['data'][0]['embedding']
# # Store embedding in DB
# def store_embedding(doc_id, embedding):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     insert_query = """
#         INSERT INTO embeddings (doc_id, embedding)
#         VALUES %s
#         ON CONFLICT (doc_id) DO UPDATE SET embedding = EXCLUDED.embedding;
#     """
#     execute_values(cur, insert_query, [(doc_id, np.array(embedding).tolist())])
#     conn.commit()
#     cur.close()
#     conn.close()
# # Retrieve embedding from DB
# def get_embedding(doc_id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT embedding FROM embeddings WHERE doc_id = %s", (doc_id,))
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     if result:
#         return np.array(result[0])
#     return None
# Example usage
# text = "Sample text to embed" 
# embedding = azure_get_embedding(text)
# store_embedding(1, embedding)
# retrieved_embedding = get_embedding(1)    
# print(retrieved_embedding)

