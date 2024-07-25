import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"
# postgres url if we decide to use postgres later on
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

# engine = create_engine(dbUrl, connect_args={'check_same_thread': False}, echo=True

engine = create_engine(
    # connect_args only needed for SQLite
    dbUrl,
    connect_args={"check_same_thread": False},
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
