from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from sqlalchemy import text
from db import get_engine
from screener import screen_resume
from utils import extract_text_docling

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(RESULTS_FOLDER, "good"), exist_ok=True)
os.makedirs(os.path.join(RESULTS_FOLDER, "bad"), exist_ok=True)

engine = get_engine()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            text = extract_text_docling(file_path)
            label, score = screen_resume(file_path, RESULTS_FOLDER)

            # Log screening result
            # with engine.begin() as conn:
            #     conn.execute(
            #         f"CREATE TABLE IF NOT EXISTS resumes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER, result TEXT, created_at datetime)"
            #         if "sqlite" in str(engine.url)
            #         else f"CREATE TABLE IF NOT EXISTS resumes (id SERIAL PRIMARY KEY, name TEXT, score INTEGER, result TEXT, created_at datetime)"
            #     )
            #     conn.execute(
            #         "INSERT INTO resumes (name, score, result, created_at) VALUES (%s, %s, %s, %s)",
            #         (file.filename, score, label, datetime.now().isoformat())
            #         if "postgres" in str(engine.url)
            #         else (file.filename, score, label, datetime.now().isoformat()),
            #     )


        # with engine.begin() as conn:
        #     # Create table
        #     if "sqlite" in str(engine.url):
        #         conn.execute(text("""
        #             CREATE TABLE IF NOT EXISTS resumes (
        #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 name TEXT,
        #                 score INTEGER,
        #                 result TEXT,
        #                 created_at TEXT
        #             )
        #         """))
        #     else:
        #         conn.execute(text("""
        #             CREATE TABLE IF NOT EXISTS resumes (
        #                 id SERIAL PRIMARY KEY,
        #                 name TEXT,
        #                 score INTEGER,
        #                 result TEXT,
        #                 created_at TIMESTAMP
        #             )
        #         """))

        #     # Insert record safely
        #     insert_stmt = text("""
        #         INSERT INTO resumes (name, score, result, created_at)
        #         VALUES (:name, :score, :result, :created_at)
        #     """)

        #     conn.execute(
        #         insert_stmt,
        #         {
        #             "name": file.filename,
        #             "score": score,
        #             "result": label,
        #             "created_at": datetime.now().isoformat()
        #         }
        #     )
        from sqlalchemy import Table, Column, Integer, String, MetaData, insert

        metadata = MetaData()
        resumes = Table(
            "resumes",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String),
            Column("score", Integer),
            Column("result", String),
            Column("created_at", String),
        )

        with engine.begin() as conn:
            metadata.create_all(engine)  # create table if not exists
            stmt = insert(resumes).values(
                name=file.filename,
                score=score,
                result=label,
                created_at=datetime.now().isoformat()
            )
            conn.execute(stmt)


            return render_template("index.html", msg=f"Resume '{file.filename}' classified as {label} (Score: {score})")

    return render_template("index.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000) # Run on port 5000

