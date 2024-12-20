from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import json

from app import db
from model.VideoClipModel import VideoClip
from model.VideoModel import Video
from repository.SqlAlchemyRepository import SqlAlchemyRepository

sqlAlchemyRepository = SqlAlchemyRepository()

class FileService:
  def videoSplit(self,videoPath,originalFilename,segmentSaveDir, segmentDuration):
    try:
      clip = VideoFileClip(videoPath)  # 원본 영상 로드
    except Exception as e:
      return {"error": f"Video loading failed: {e}"}

    duration = clip.duration  # 전체 영상 길이 (초 단위)
    segments = []
    startTime = 0

    while startTime < duration:
      endTime = min(startTime + segmentDuration, duration)  # 끝나는 시간 계산
      segment = clip.subclipped(startTime, endTime)  # 특정 구간 클립 추출
      segmentName = f"{originalFilename}_{int(startTime)}_{int(endTime)}.mp4"

      segmentPath = os.path.join(segmentSaveDir, segmentName) # 문자열 경로 생성
      try:
        segment.write_videofile(segmentPath, codec="libx264", audio_codec="aac")  # 저장
      except Exception as e:
        return {"error": f"Video saving failed: {e}"}

      segments.append({
        "startTime": f"{int(startTime // 60)}분 {int(startTime % 60)}초",
        "endTime": f"{int(endTime // 60)}분 {int(endTime % 60)}초",
        "videoName": segmentName,
        "segmentPath": segmentPath
      })
      startTime = endTime

    clip.close()

    videoDataResult = self.allVideoSave(originalFilename,segments)  # 분리된 영상 정보들 DB에 저장하는 작업
    for idx,videoData in enumerate(videoDataResult):
      segments[idx]["videoId"] = videoData.id

    return segments



  def allVideoSave(self,originalFilename,segments):
    videoList = []
    for segment in segments:
      videoList.append(Video(
          # video_id=,
          title=originalFilename,
          file_name=segment["videoName"],
          video_url=segment["segmentPath"],
          play_time=0,
      ))

    sqlAlchemyRepository.saveAll(videoList)

    return videoList