from flask import g
from model.VideoCaptioningModel import VideoCaptioning

class VideoCaptioningRepository:
  ":return: VideoCaptioning 객체들의 리스트"
  def findByVideoId(self,videoIdList):
    return g.db.session.query(VideoCaptioning).filter(VideoCaptioning.video_id.in_(videoIdList)).all()