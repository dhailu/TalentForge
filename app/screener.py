import os, shutil, numpy as np
from dotenv import load_dotenv
load_dotenv()
from db import SessionLocal
from models import ResumeMetadata
from embedding import azure_get_embedding

THRESHOLD = float(os.getenv("SCREEN_THRESHOLD", "0.75"))

def cosine_similarity(a, b):
    a = np.array(a); b = np.array(b)
    if np.linalg.norm(a)==0 or np.linalg.norm(b)==0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def screen_resumes(job_text, days=None, job_id=None):
    job_emb = azure_get_embedding(job_text)
    db = SessionLocal()
    try:
        query = db.query(ResumeMetadata)
        # optional filters could be applied here (job_id, date range)
        rows = query.all()
        os.makedirs("uploads/good", exist_ok=True)
        os.makedirs("uploads/bad", exist_ok=True)
        good, bad = [], []
        for r in rows:
            if not r.embedding:
                bad.append((r.filename, 0.0))
                continue
            sim = cosine_similarity(r.embedding, job_emb)
            if sim >= THRESHOLD:
                try:
                    shutil.copy(f"uploads/{r.filename}", f"uploads/good/{r.filename}")
                except:
                    pass
                good.append((r.filename, sim))
            else:
                try:
                    shutil.copy(f"uploads/{r.filename}", f"uploads/bad/{r.filename}")
                except:
                    pass
                bad.append((r.filename, sim))
        return {"good": good, "bad": bad}
    finally:
        db.close()
