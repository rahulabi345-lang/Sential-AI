from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = Path(__file__).parent / "sentinel.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# create_engine initializes SQLite database connection
# check_same_thread=False allows SQLite to work with FastAPI multithreaded requests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy ORM models
Base = declarative_base()


def get_db():
    """Dependency function to get database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

