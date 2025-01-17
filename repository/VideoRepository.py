from flask import g
from model.VideoModel import Video

class VideoRepository:
  def findByVideoId(self, videoId):
    return g.db.session.query(Video).filter(Video.id == videoId).first()

  def updateChromaCollectionNameIds(self, videoIdList, collectionName):
    g.db.session.query(Video).filter(Video.id.in_(videoIdList)).update(
        {Video.chroma_collection_name: collectionName}, synchronize_session=False #세션을 즉시 동기화하지 않도록 설정
    )
    g.db.session.commit()