from sqlalchemy import Column, Integer, String, DateTime, JSON
from database import Base, DB_PATH
import sqlite3


class SecurityEvent(Base):
    """SQLAlchemy model for the security_events database table."""

    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String, nullable=False)
    source = Column(String, nullable=False)
    hostname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    process_name = Column(String, nullable=False)
    process_id = Column(Integer, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(String, nullable=False)
    raw_data = Column(JSON, nullable=True)
    risk_score = Column(Integer, nullable=True, default=0)
    risk_level = Column(String, nullable=True, default="LOW")
    risk_reasons = Column(JSON, nullable=True, default=list)

    # AI Analyzer fields
    ai_title = Column(String, nullable=True)
    ai_summary = Column(String, nullable=True)
    ai_explanation = Column(String, nullable=True)
    ai_indicators = Column(JSON, nullable=True, default=list)
    ai_recommended_actions = Column(JSON, nullable=True, default=list)
    ai_confidence = Column(Integer, nullable=True, default=0)


def auto_migrate():
    """Ensures existing SQLite database table has risk and AI analysis fields if created previously."""
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(security_events)")
            columns = [col[1] for col in cursor.fetchall()]
            if columns:
                if "risk_score" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN risk_score INTEGER DEFAULT 0")
                if "risk_level" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN risk_level TEXT DEFAULT 'LOW'")
                if "risk_reasons" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN risk_reasons TEXT DEFAULT '[]'")
                if "ai_title" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN ai_title TEXT")
                if "ai_summary" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN ai_summary TEXT")
                if "ai_explanation" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN ai_explanation TEXT")
                if "ai_indicators" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN ai_indicators TEXT DEFAULT '[]'")
                if "ai_recommended_actions" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN ai_recommended_actions TEXT DEFAULT '[]'")
                if "ai_confidence" not in columns:
                    cursor.execute("ALTER TABLE security_events ADD COLUMN ai_confidence INTEGER DEFAULT 0")
                conn.commit()
            conn.close()
        except Exception:
            pass


auto_migrate()

