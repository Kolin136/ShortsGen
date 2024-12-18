import os
import time
from flask import current_app, jsonify
import google.generativeai as genai
import re
import json

class GeminiService:
  prompt = ("이 업로드 영상을 5초 단위로 분석하는데 다음과 같은 형태의 결과로 출력줘, "
           "출력의 형태는 json 포맷으로 키(영문으로), 값(한국어로)의 형태고, "
           "키의 종류는 분석 하는 영상 파일 정확한 이름(확장자까지 포함),영상 요약, 영상시작시간, 영상 종료기간, 분위기, 등장인물등의 주요 정보들을 포함시켜줘. "
           "전체 비디오에 대한 요약 말고 무조건 5초 단위로해")
  def videoCaptioning(self,gemini_llm,fileNameList):
    # JSON 데이터 검증
    if not fileNameList:
      return jsonify({"error": "파일 이름 목록이 제공되지 않았습니다."}), 400


    # 'segments' 폴더에서 파일 찾기
    segments_folder = os.path.normpath("./static/video/segments")  # 경로 표준화
    files_to_process = []

    for fileName in fileNameList:
      file_path = os.path.normpath(os.path.join(segments_folder, fileName)) # OS에 맞는 경로 조합
      if os.path.exists(file_path):
        files_to_process.append(file_path)
      else:
        return jsonify({"error": f"파일 '{fileName}'을 찾을 수 없습니다."}), 404


    chat_session = gemini_llm.start_chat(history=[])
    result = []

    for idx,file_path in enumerate(files_to_process):
      uploadFile = self.uploadToGemini(file_path, mime_type="video/mp4")
      response = chat_session.send_message([self.prompt,uploadFile])

      # LLM 응답받은 문자열을 정규식으로 JSON 리스트 추출
      match = re.search(r'\[\s*{.*?}\s*\]', response.text, re.DOTALL)

      if match:
        json_list_str = match.group()  # JSON 리스트 부분만 추출
        try:
          json_list = json.loads(json_list_str)  # 문자열을 Python 리스트로 변환
          # 각 딕셔너리에 "videoName" 키 추가
          for item in json_list:
            item["videoName"] = fileNameList[idx]  # videoName에 파일 경로 추가

          result.extend(json_list)  # 파싱된 리스트를 결과 리스트에 추가
        except json.JSONDecodeError:
          return jsonify({"error": "응답 JSON 형식이 잘못되었습니다. 다시 시도해 주세요."}), 500
      else:
        return jsonify({"error": "Json형식 응답받지 못했거나 LLM 서버의 중간 오류가 있었습니다. 다시 요청 해주세요"}), 500

    return result



  def uploadToGemini(self,path, mime_type=None):
    video_file = genai.upload_file(path, mime_type=mime_type)
    while video_file.state.name == "PROCESSING":
      current_app.logger.info('Waiting for video to be processed.')
      time.sleep(10)
      video_file = genai.get_file(video_file.name)

    return video_file

