from flask import g
from model.VideoModel import Video

class VideoRepository:
  def findAllByVideoIds (self, videoIdList):
    return g.db.session.query(Video).filter(Video.id.in_(videoIdList)).all()

  def findByOriginalVideoName(self, originalVideoName):
    return g.db.session.query(Video).filter(Video.original_video_name == originalVideoName).all()


