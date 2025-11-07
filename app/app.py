import os, tempfile, uuid
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
load_dotenv()

from db import init_db, SessionLocal
from azure_storage_client import upload_to_adls
from extractor import extract_text_local, sanitize_text
from docling_client import DoclingClient
from virus_scan import scan_file
from embedding import azure_get_embedding
from models import ResumeMetadata
from screener import screen_resumes

# init
init_db()
app = Flask(__name__, template_folder="templates")
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# optionally use docling if configured
use_docling = bool(os.getenv("DOCLING_URL"))
if use_docling:
    docling = DoclingClient()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    filename = f.filename
    local_path = os.path.join(UPLOAD_DIR, filename)
    f.save(local_path)

    # 1. virus scan
    clean, reason = scan_file(local_path)
    if not clean:
        return jsonify({"error": "file failed virus scan", "reason": reason}), 400

    # 2. parse (docling if configured else local)
    try:
        if use_docling:
            text = docling.parse(local_path)
        else:
            text = extract_text_local(local_path)
    except Exception as e:
        return jsonify({"error": "parsing failed", "detail": str(e)}), 500

    # 3. sanitize
    text_clean = sanitize_text(text)

    # 4. upload raw to ADLS (blob path)
    try:
        blob_path = upload_to_adls(local_path, f"raw/{uuid.uuid4().hex}_{filename}")
    except Exception as e:
        return jsonify({"error": "upload failed", "detail": str(e)}), 500

    # 5. generate embedding
    try:
        emb = azure_get_embedding(text_clean)
    except Exception as e:
        return jsonify({"error": "embedding failed", "detail": str(e)}), 500

    # 6. persist to DB
    from db import SessionLocal
    db = SessionLocal()
    try:
        rec = ResumeMetadata(
            filename=filename,
            blob_path=blob_path,
            text_content=text_clean,
            embedding=emb
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
    finally:
        db.close()

    return jsonify({"message": "uploaded", "id": rec.id, "filename": filename}), 201

@app.route("/screen-resumes", methods=["POST"])
def screen():
    body = request.get_json()
    if not body or "job_description" not in body:
        return jsonify({"error":"job_description required"}), 400
    job_text = body["job_description"]
    res = screen_resumes(job_text)
    return jsonify({"summary": {"good": len(res["good"]), "bad": len(res["bad"])}, "details": res})

@app.route("/health")
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "8000"))
    app.run(host=host, port=port)
