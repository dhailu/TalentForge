import os
import requests
from dotenv import load_dotenv
load_dotenv()

AZ_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/")
AZ_KEY = os.getenv("AZURE_OPENAI_API_KEY")
EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
MAX_LEN = int(os.getenv("AZURE_EMBED_MAX_LENGTH", "2000"))

def azure_get_embedding(text):
    text = text[:MAX_LEN]
    url = f"{AZ_ENDPOINT}/openai/deployments/{EMBED_MODEL}/embeddings?api-version=2024-10-01"
    headers = {"api-key": AZ_KEY, "Content-Type": "application/json"}
    payload = {"input": text}
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    res = r.json()
    return res["data"][0]["embedding"]

os.path.dirname('updates')
