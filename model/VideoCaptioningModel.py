from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db
from sqlalchemy.dialects.mysql import JSON

class VideoCaptioning(db.Model):
  __tablename__ = 'video_captioning'

  # Primary Key
  id = Column(Integer, primary_key=True, autoincrement=True, name="video_captioning_id")

  # Foreign Key: Video ID
  video_id = Column(Integer, ForeignKey('video.video_id', ondelete='CASCADE'), nullable=False)

  # Foreign Key: Prompt ID
  prompt_id = Column(Integer, ForeignKey('prompt.prompt_id'), nullable=False)

  # VectorDb Collection Name
  chroma_collection_name = Column(String(255), nullable=True)

  video_analysis_json = Column(JSON, nullable=True)

  timecode = Column(String(100), nullable=False)

  start_time = Column(String(100), nullable=False, name="start_time")

  end_time = Column(String(100), nullable=False, name="end_time")

  created_at = Column(DateTime, default=datetime.utcnow, nullable=False, name="created_at")

  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, name="updated_at")




