import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Vercel serverless filesystem is read-only except /tmp.
    if os.getenv("VERCEL"):
        local_db = Path("/tmp/smartcampus.db")
    else:
        local_db = Path(__file__).resolve().parents[1] / "smartcampus.db"
    DATABASE_URL = f"sqlite:///{local_db.as_posix()}"
    print(f"INFO: DATABASE_URL not set. Falling back to {DATABASE_URL}")

# Some providers still hand out postgres:// URLs; SQLAlchemy expects postgresql://.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
