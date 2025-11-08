# import os, requests
# from dotenv import load_dotenv
# load_dotenv()

# DOCLING_URL = os.getenv("DOCLING_URL")
# DOCLING_API_KEY = os.getenv("DOCLING_API_KEY")

# class DoclingClient:
#     def __init__(self):
#         self.url = DOCLING_URL
#         self.api_key = DOCLING_API_KEY

#     def parse(self, file_path):
#         if not self.url:
#             raise ValueError("DOCLING_URL not configured")
#         headers = {}
#         if self.api_key:
#             headers["Authorization"] = f"Bearer {self.api_key}"
#         with open(file_path, "rb") as f:
#             files = {'file': f}
#             r = requests.post(self.url, headers=headers, files=files, timeout=120)
#             r.raise_for_status()
#             data = r.json()
#             sections = data.get("sections", [])
#             return " ".join([s.get("content","") for s in sections])
