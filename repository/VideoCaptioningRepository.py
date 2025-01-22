from flask import g
from model.VideoCaptioningModel import VideoCaptioning
from model.VideoModel import Video

class VideoCaptioningRepository:
  ":return: VideoCaptioning 객체들의 리스트"
  def findByVideoId(self,videoIdList):
    return g.db.session.query(VideoCaptioning).filter(VideoCaptioning.video_id.in_(videoIdList)).all()

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