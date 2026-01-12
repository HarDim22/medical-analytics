from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(64), index=True, nullable=False)
    entity_id = Column(String(128), index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), index=True, nullable=False)
    actor_role = Column(String(32), nullable=True)

    # IMPORTANT: 'metadata' is reserved in SQLAlchemy
    event_data = Column("metadata", JSON, nullable=False)

