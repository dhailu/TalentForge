import os
import requests

def extract_text_docling(file_path):
    url = os.getenv("DOCLING_URL")
    api_key = os.getenv("DOCLING_API_KEY")

    if not url or not api_key:
        return "Docling not configured."

    with open(file_path, "rb") as f:
        files = {"file": f}
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        return response.json().get("content", "")
    else:
        return f"Error: {response.text}"
