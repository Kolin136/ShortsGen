from flask import g
from model.VideoClipModel import VideoClip

class VideoClipRepository:
  ":return: VideoClip 객체들의 리스트"
  def findByVideoId(self,videoIdList):
    return g.db.session.query(VideoClip).filter(VideoClip.video_id.in_(videoIdList)).all()