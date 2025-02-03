from flask import g
from model.VideoModel import Video

class VideoRepository:
  def findByVideoId(self, videoId):
    return g.db.session.query(Video).filter(Video.id == videoId).first()

  def findByVideoChromaCollectionName(self, collectionName):
    return g.db.session.query(Video).filter(Video.chroma_collection_name == collectionName).first()

  def findByOriginalVideoName(self, originalVideoName):
    return g.db.session.query(Video).filter(Video.original_video_name == originalVideoName).all()


