from flask import g
from model.VideoModel import Video

class VideoRepository:
  def findByVideoId(self, videoId):
    return g.db.session.query(Video).filter(Video.id == videoId).first()