from moviepy.video.io.VideoFileClip import VideoFileClip
import os

class FileService:
  def fileSplit(self,video_path, output_dir, segment_duration):
    try:
      clip = VideoFileClip(video_path)  # 원본 영상 로드
    except Exception as e:
      return {"error": f"Video loading failed: {e}"}

    duration = clip.duration  # 전체 영상 길이 (초 단위)
    segments = []
    start_time = 0
    while start_time < duration:
      end_time = min(start_time + segment_duration, duration)  # 끝나는 시간 계산
      segment = clip.subclipped(start_time, end_time)            # 특정 구간 클립 추출

      output_file = os.path.join(output_dir, f"segment_{int(start_time)}_{int(end_time)}.mp4")
      try:
        segment.write_videofile(output_file, codec="libx264", audio_codec="aac")  # 저장
      except Exception as e:
        return {"error": f"Video saving failed: {e}"}

      segments.append({
        "start_time": f"{int(start_time // 60)}분 {int(start_time % 60)}초",
        "end_time": f"{int(end_time // 60)}분 {int(end_time % 60)}초",
        "file_path": output_file
      })
      start_time = end_time

    clip.close()
    return segments
