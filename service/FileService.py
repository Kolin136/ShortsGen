from moviepy.video.io.VideoFileClip import VideoFileClip
import os

class FileService:
  def videoSplit(self,videoPath,filename,segmentSaveDir, segmentDuration):
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
      segmentName = f"{filename}_{int(startTime)}_{int(endTime)}.mp4"

      segmentPath = os.path.join(segmentSaveDir, segmentName) # 문자열 경로 생성
      try:
        segment.write_videofile(segmentPath, codec="libx264", audio_codec="aac")  # 저장
      except Exception as e:
        return {"error": f"Video saving failed: {e}"}

      segments.append({
        "startTime": f"{int(startTime // 60)}분 {int(startTime % 60)}초",
        "endTime": f"{int(endTime // 60)}분 {int(endTime % 60)}초",
        "videoName": segmentName
      })
      startTime = endTime

    clip.close()
    
    return segments
