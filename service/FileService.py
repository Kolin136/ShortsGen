from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from model.celeryModel.CeleryVideoModel import Video
from repository.SqlAlchemyRepository import SqlAlchemyRepository
from moviepy import VideoFileClip, concatenate_videoclips

from repository.VideoRepository import VideoRepository

sqlAlchemyRepository = SqlAlchemyRepository()
videoRepository = VideoRepository()

class FileService:
  def videoSplit(self,videoPath,originalFilename,segmentSaveDir,segmentDuration):
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
        "videoName": segmentName,
        "segmentPath": segmentPath
      })
      startTime = endTime

    clip.close()

    videoDataResult = self.allVideoSave(segments,originalFilename)  # 분리된 영상 정보들 DB에 저장하는 작업
    for idx,videoData in enumerate(videoDataResult):
      segments[idx]["videoId"] = videoData.id

    return segments


  def videoMerge(self, videoDatas,createVideoName):
    # 타임코드 문자열을 초 단위로 변환
    def timeToSeconds(timeStr):
      m, s = map(int, timeStr.split(":"))
      return m * 60 + s

    # 데이터 정렬 (video_id,start_time 순으로 정렬 기준)
    videoDatasSort = sorted(
        videoDatas,  # 정렬 대상
        key=lambda x: (x["video_id"], timeToSeconds(x["start_time"]))  # 1차: video_id, 2차: start_time
    )

    # videoDatas에 비디오들 합치기 위해 분리된 비디오 정보 가져오기 위한 작업
    videoIdSet = set()
    for data in videoDatas:
      videoIdSet.add(data["video_id"])

    videoModelList = videoRepository.findAllByVideoIds(videoIdSet)
    videoSplitData = {videoModel.id: videoModel for videoModel in videoModelList}

    # 각 비디오 일부분 자르고 결합 작업 시작
    clips = []
    for videoData in videoDatasSort:
      startTime = videoData["start_time"]
      endTime = videoData["end_time"]
      startSeconds = timeToSeconds(startTime)
      endSeconds = timeToSeconds(endTime)

      videoFileUrl = videoSplitData[videoData["video_id"]].video_url

      # MoviePy로 해당 구간의 비디오 클립 생성
      clip = VideoFileClip(videoFileUrl).subclipped(start_time=startSeconds, end_time=endSeconds)
      clips.append(clip)

    # Step 3: 클립 합치기
    finalClip = concatenate_videoclips(clips, method="chain")  # 클립들의 해상도나 FPS가 동일하지 않으면 method="compose"로 변경

    # Step 4: 결과 비디오 저장
    finalVideoPath = f"./static/video/merge/{createVideoName}_shorts.mp4"
    finalClip.write_videofile(finalVideoPath, codec="libx264", fps=24)

    return finalVideoPath


  def videoSplitSearch(self, originalVideoName):
    videoModelList = videoRepository.findByOriginalVideoName(originalVideoName)
    result = []
    for videoModel in videoModelList:
      result.append(
          {
            "videoId": str(videoModel.id),
            "videoName": videoModel.file_name,
          }
      )

    return result




  def allVideoSave(self,segments,originalFilename):
    videoList = []
    for segment in segments:
      videoList.append(Video(
          file_name=segment["videoName"],
          video_url=segment["segmentPath"],
          original_video_name=originalFilename
      ))

    sqlAlchemyRepository.celerySaveAll(videoList)

    return videoList

