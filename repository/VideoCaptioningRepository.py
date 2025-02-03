from flask import g
from model.VideoCaptioningModel import VideoCaptioning
from model.VideoModel import Video

class VideoCaptioningRepository:
  ":return: VideoCaptioning 객체들의 리스트"
  def findByPromptId(self,promptId):
    return g.db.session.query(VideoCaptioning).filter(VideoCaptioning.prompt_id == promptId).all()

  def findByVideoCollectionNameWithJoin(self, collection_name):
    """
    collection_name에 해당하는 비디오 중 하나를 가져오고,
    JOIN을 사용하여 해당 비디오의 VideoCaptioning 데이터 한개 가져온다.

    :return: VideoCaptioning 객체 또는 None (해당 데이터가 없을 경우)
    """
    videoCaptioning = g.db.session.query(VideoCaptioning). \
      join(Video, Video.id == VideoCaptioning.video_id). \
      filter(Video.chroma_collection_name.contains(collection_name)). \
      first()

    return videoCaptioning

  def findByVideoIdAndPromptId(self, videoId, promptId):
    return g.db.session.query(VideoCaptioning).filter(
        VideoCaptioning.video_id == videoId,
        VideoCaptioning.prompt_id == promptId
    ).all()

  def deleteByVideoIdAndPromptId(self, videoId, promptId):
    g.db.session.query(VideoCaptioning).filter(
        VideoCaptioning.video_id == videoId,
        VideoCaptioning.prompt_id == promptId
    ).delete()
    g.db.session.commit()


  def updateChromaCollectionNameIds(self, promptId, collectionName):
    g.db.session.query(VideoCaptioning).filter(VideoCaptioning.prompt_id == promptId).update(
        {VideoCaptioning.chroma_collection_name: collectionName}, synchronize_session=False #세션을 즉시 동기화하지 않도록 설정
    )
    g.db.session.commit()

  def findChromaCollectionByPromptId(self, promptId):
    return g.db.session.query(VideoCaptioning) \
      .filter(VideoCaptioning.prompt_id == promptId) \
      .filter(VideoCaptioning.chroma_collection_name.isnot(None)) \
      .order_by(VideoCaptioning.id.desc()) \
      .limit(1) \
      .first()