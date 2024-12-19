from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db

class VideoClip(db.Model):
  __tablename__ = 'video_clip'

  # Primary Key
  id = Column(Integer, primary_key=True, autoincrement=True, name="video_clip_id")

  # Foreign Key: Video ID
  video_id = Column(Integer, ForeignKey('video.video_id', ondelete='CASCADE'), nullable=False)

  # Summary information
  summary = Column(String(800), nullable=False)

  # Start time
  start_time = Column(String(100), nullable=False, name="start_time")

  # End time
  end_time = Column(String(100), nullable=False, name="end_time")

  # Created at timestamp
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False, name="created_at")

  # Updated at timestamp (auto-updated)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, name="updated_at")

  # Relationship to Video
  video = relationship("Video", back_populates="video_clips")

  # Index definition
  __table_args__ = (
    Index('ix_video_clip_video_id', "video_id", postgresql_using='btree'),
  )

  # __init__ 메서드
  def __init__(self, video_id, summary, start_time, end_time):
    """
    VideoClip 객체를 생성할 때 기본 속성 값을 초기화합니다.
    """
    self.video_id = video_id
    self.summary = summary
    self.start_time = start_time
    self.end_time = end_time

  # __repr__ 메서드
  def __repr__(self):
    """
    VideoClip 객체를 문자열로 표현합니다.
    """
    return (
      f"<VideoClip(id={self.id}, video_id={self.video_id}, "
      f"summary='{self.summary[:50]}', start_time='{self.start_time}', "
      f"end_time='{self.end_time}', created_at={self.created_at})>"
    )