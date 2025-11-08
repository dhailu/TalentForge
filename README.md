# Resume AI Screening System

An AI-powered resume screening system using Flask, PostgreSQL/SQLite, and Docker.  
Uploads are analyzed and classified into "good" or "bad" based on model/keyword analysis.

###  Features
- Upload and analyze PDF/DOC resumes
- Store screening results in SQLite or PostgreSQL
- Integrate with Docling or LLM for text extraction
- View and manage uploaded resumes
- Auto-save “Good” and “Bad” results

###  Run

```bash
docker-compose up --build
