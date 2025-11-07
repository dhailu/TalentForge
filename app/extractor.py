import pdfplumber
from docx import Document
import re

def extract_text_local(file_path):
    text = ""
    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif file_path.lower().endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return text

# sanitize: remove URLs and optionally mask emails
def sanitize_text(text, mask_pii=True):
    # remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "[LINK]", text)
    if mask_pii:
        # mask emails
        text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL]", text)
        # mask phone numbers (basic)
        text = re.sub(r"(\+\d{1,3}\s?)?(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})", "[PHONE]", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text
