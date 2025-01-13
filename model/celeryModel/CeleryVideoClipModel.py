from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from celeryApp import celeryDb

class VideoClip(celeryDb.Model):
  __tablename__ = 'video_clip'

  # Primary Key
  id = Column(Integer, primary_key=True, autoincrement=True, name="video_clip_id")

  # Foreign Key: Video ID
  video_id = Column(Integer, ForeignKey('video.video_id', ondelete='CASCADE'), nullable=False)

  characters = Column(String(255), nullable=False)

  scene = Column(String(800), nullable=False)

  emotion = Column(String(255), nullable=False)

  summary = Column(String(500), nullable=False)

  action = Column(String(500), nullable=False)

  scene_description = Column(String(500), nullable=False)

  timecode = Column(String(100), nullable=False)

  # Start time
  start_time = Column(String(100), nullable=False, name="start_time")

  # End time
  end_time = Column(String(100), nullable=False, name="end_time")

  # Created at timestamp
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False, name="created_at")

  # Updated at timestamp (auto-updated)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, name="updated_at")


  # Index definition
  __table_args__ = (
    Index('ix_video_clip_video_id', "video_id", postgresql_using='btree'),
  )


  # __repr__ 메서드
  def __repr__(self):
    """
    VideoClip 객체를 문자열로 표현합니다.
    """
    return (
      f"<VideoClip(id={self.id}, video_id={self.video_id}, "
      f"summary='{self.summary[:50]}', mood='{self.mood}', characters='{self.characters}', "
      f"start_time='{self.start_time}', end_time='{self.end_time}', created_at={self.created_at})>"
    )