from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db

class Video(db.Model):
  __tablename__ = 'video'

  # Primary Key
  id = Column(Integer, primary_key=True, autoincrement=True, name="video_id")

  # Video title
  title = Column(String(255), nullable=False)

  # File name
  file_name = Column(String(255), nullable=False)

  # Video URL
  video_url = Column(String(255), nullable=False)

  # Play time
  play_time = Column(Integer, default=0, nullable=False)

  # Created at timestamp
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

  # Updated at timestamp (auto-updated)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

  # Relationship with VideoClip
  video_clips = relationship("VideoClip", backref="video",lazy=True)  # 일대다(1:N) 관계를 정의 , backref는 역방향 참조(VideoClip에서 video 참조 가능하게)

  # __repr__ 메서드
  def __repr__(self):
    """
    Video 객체를 문자열로 표현합니다.
    """
    return (
      f"<Video(id={self.id}, title='{self.title}', "
      f"file_name='{self.file_name}', video_url='{self.video_url}', "
      f"play_time={self.play_time}, created_at={self.created_at})>"
    )