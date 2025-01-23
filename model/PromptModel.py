from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import JSON

class Prompt(db.Model):
  __tablename__ = 'prompt'

  # Primary Key
  id = Column(Integer, primary_key=True, autoincrement=True, name="prompt_id")

  title = Column(String(255),nullable=True)

  prompt_text = Column(String(10000),nullable=False)

  created_at = Column(DateTime, default=datetime.utcnow, nullable=False, name="created_at")

  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, name="updated_at")

  # Relationship with VideoCationing
  video_captionings = relationship("VideoCaptioning", backref="prompt",lazy=True)