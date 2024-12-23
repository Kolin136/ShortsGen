import os
import time
from flask import current_app, jsonify
import google.generativeai as genai
import re
import json
from model.VideoClipModel import VideoClip
from repository.SqlAlchemyRepository import SqlAlchemyRepository
from repository.VideoClipRepository import VideoClipRepository

sqlAlchemyRepository = SqlAlchemyRepository()
videoClipRepository = VideoClipRepository()

class GeminiService:
  def __init__(self):
    promptPath = "./prompt.txt"
    with open(promptPath, "r", encoding="utf-8") as file:
      self.prompt = file.read()

  def videoCaptioning(self,gemini_llm,segmentsList):
    # JSON 데이터 검증
    if not segmentsList:
      return jsonify({"error": "파일 이름 목록이 제공되지 않았습니다."}), 400


    # 'segments' 폴더에서 파일 찾기
    segments_folder = os.path.normpath("./static/video/segments")  # 경로 표준화
    files_to_process = []

    for segment in segmentsList:
      file_path = os.path.normpath(os.path.join(segments_folder, segment["videoName"])) # OS에 맞는 경로 조합
      if os.path.exists(file_path):
        files_to_process.append(file_path)
      else:
        return jsonify({"error": f"파일 '{segment['videoName']}'을 찾을 수 없습니다."}), 404


    chat_session = gemini_llm.start_chat(history=[])
    result = []

    for idx,file_path in enumerate(files_to_process):
      try:
        uploadFile = self.uploadToGemini(file_path, mime_type="video/mp4")
      except Exception as e:
        error_response = {
          "error": "Video Processing Failed",
          "details": str(e)
        }
        return jsonify(error_response), 500 # 500 Internal Server Error

      #임시 정적 이미지 업로드
      promptList = [self.prompt,uploadFile]
      imageList = ["김도기.PNG","박양진.PNG","안부장.PNG","이춘식.PNG","정이사.PNG"]
      image_folder = os.path.normpath("./static/image")
      for image in imageList:
        image_path = os.path.normpath(os.path.join(image_folder, image))
        uploadImage = self.uploadToGemini(image_path, mime_type="image/png")
        promptList.append(uploadImage)

      response = chat_session.send_message(promptList)

      print("결과->\n",response.text)

      # LLM 응답받은 문자열을 정규식으로 JSON 리스트 추출
      match = re.search(r'\[\s*{.*?}\s*\]', response.text, re.DOTALL)

      if match:
        json_list_str = match.group()  # JSON 리스트 부분만 추출
        try:
          json_list = json.loads(json_list_str)  # 문자열을 Python 리스트로 변환
          # 각 딕셔너리에 "videoName","videoId" 키 추가
          for item in json_list:
            item["videoName"] = segmentsList[idx]["videoName"]  # videoName에 파일 경로 추가
            item["videoId"] = segmentsList[idx]["videoId"]

          result.extend(json_list)  # 파싱된 리스트를 결과 리스트에 추가
        except json.JSONDecodeError:
          return jsonify({"error": "응답 JSON 형식이 잘못되었습니다. 다시 시도해 주세요."}), 500
      else:
        return jsonify({"error": "Json형식 응답받지 못했거나 LLM 서버의 중간 오류가 있었습니다. 다시 요청 해주세요"}), 500



    return result


  def geminiCaptioningSave(self, videoAnalysisData):
    VideoClipList = []
    for clipData in videoAnalysisData:
        # VideoClipModel 객체 생성 및 매핑
        VideoClipList.append(VideoClip(
            video_id=int(clipData["videoId"]),
            characters=",".join(clipData["characters"]),
            scene=",".join(clipData["scene"]),
            emotion=",".join(clipData["emotion"]),
            summary=",".join(clipData["summary"]),
            action=",".join(clipData["action"]),
            scene_description=",".join(clipData["scene_description"]),
            timecode=clipData["timecode"],
            start_time=clipData["start_time"],
            end_time=clipData["end_time"])
        )

    sqlAlchemyRepository.saveAll(VideoClipList)


  def uploadToGemini(self,path, mime_type=None):
    video_file = genai.upload_file(path, mime_type=mime_type)
    while video_file.state.name == "PROCESSING":
      current_app.logger.info('Waiting for video to be processed.')
      time.sleep(10)
      video_file = genai.get_file(video_file.name)

    if video_file.state.name != "ACTIVE":
      raise Exception(f"File {video_file.name} upload failed to process")

    print(video_file,"업로드 성공")
    return video_file






