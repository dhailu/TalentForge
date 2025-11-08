import os
from sqlalchemy import create_engine
from pathlib import Path

def get_engine():
    """
    Dynamically create SQLAlchemy engine.
    - Supports SQLite (default) and PostgreSQL.
    - Ensures SQLite directory exists.
    """
    db_type = os.getenv("DB_TYPE", "sqlite").lower()

    try:
        if db_type == "postgres":
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            host = os.getenv("POSTGRES_HOST", "localhost")
            db = os.getenv("POSTGRES_DB", "resume_ai_db")
            port = os.getenv("POSTGRES_PORT", "5432")

            url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
            print(f"Connecting to PostgreSQL at {host}:{port}/{db}")
        
        else:
            # Default to SQLite
            sqlite_path = os.getenv("SQLITE_DB_PATH", "data/sqlite.db")
            Path(os.path.dirname(sqlite_path)).mkdir(parents=True, exist_ok=True)

            url = f"sqlite:///{sqlite_path}"
            print(f"Using SQLite at {sqlite_path}")

        # Create SQLAlchemy engine
        engine = create_engine(url, echo=False)
        return engine

    except Exception as e:
        print(f" Error creating database engine: {e}")
        raise
