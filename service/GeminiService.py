import os
import time
from flask import current_app, jsonify
import google.generativeai as genai
import re
import json
from model.VideoClipModel import VideoClip
from promptTemplate import PromptTemplate
from repository.SqlAlchemyRepository import SqlAlchemyRepository
from io import BytesIO
import types
import typing_extensions as typing

sqlAlchemyRepository = SqlAlchemyRepository()


class GeminiService:
  """
  비디오 캡셔닝 작업 
  """
  def videoCaptioning(self,gemini_llm,splitVideoList,imagesList,userPrompt,jsonFieldList):
    # JSON 데이터 검증
    if not splitVideoList:
      return jsonify({"error": "비디오가 제공되지 않았습니다."}), 400

    # 'segments' 폴더에서 파일 찾기
    segments_folder = os.path.normpath("./static/video/segments")  # 경로 표준화
    files_to_process = []

    for segment in splitVideoList:
      videoPath = os.path.normpath(os.path.join(segments_folder, segment["videoName"])) # OS에 맞는 경로 조합
      if os.path.exists(videoPath):
        files_to_process.append(videoPath)
      else:
        return jsonify({"error": f"파일 '{segment['videoName']}'을 찾을 수 없습니다."}), 404


    # chat_session = gemini_llm.start_chat(history=[])
    result = []

    promptList = []  #프롬프트에 업로드한 영상,이미지 포함시키기 위해서
    #영상 업로드 작업
    for file_path in files_to_process:
      try:
        uploadVideo = self.uploadToGemini(file_path, mime_type="video/mp4")
        promptList.append(uploadVideo)
      except Exception as e:
        error_response = {
          "error": "Video Processing Failed",
          "details": str(e)
        }
        return jsonify(error_response), 500 # 500 Internal Server Error

    # 이미지 업로드 작업
    characters = []
    for image in imagesList:
      # BytesIO로 변환
      imageByteStream = BytesIO(image.read())
      imageByteStream.seek(0)

      uploadImage = self.uploadToGemini(imageByteStream, mime_type=image.mimetype)

      promptList.append(uploadImage)
      characters.append(os.path.splitext(image.filename)[0]) # 확장자 제거)

    prompt = PromptTemplate.prompt(characters,userPrompt)
    promptList.append(prompt)

    #LLM 응답 Json형식 설정
    ResultDict = self.createResponseSchema(jsonFieldList)

    # response = chat_session.send_message(promptList) #gemini한테 요청 보내는 메소드(히스토리 자동관리 방식)
    response = gemini_llm.generate_content(promptList,generation_config=genai.GenerationConfig(temperature=0,response_mime_type="application/json", response_schema=ResultDict))

    # LLM 응답받은 문자열을 정규식으로 JSON 리스트 추출
    match = re.search(r'\[\s*{.*?}\s*\]', response.text, re.DOTALL)

    if match:
      json_list_str = match.group()  # JSON 리스트 부분만 추출
      try:
        json_list = json.loads(json_list_str)  # 문자열을 Python 리스트로 변환
        # 각 딕셔너리에 "videoName","videoId" 키 추가
        for item in json_list:
          item["videoName"] = splitVideoList[0]["videoName"]  # videoName에 파일 경로 추가
          item["videoId"] = splitVideoList[0]["videoId"]

        result.extend(json_list)  # 파싱된 리스트를 결과 리스트에 추가
      except json.JSONDecodeError:
        return jsonify({"error": "응답 JSON 형식이 잘못되었습니다. 다시 시도해 주세요."}), 500
    else:
      return jsonify({"error": "Json형식 응답받지 못했거나 LLM 서버의 중간 오류가 있었습니다. 다시 요청 해주세요"}), 500

    return result

  """
  비디오 캡셔닝 결과 DB에 저장 메소드
  """
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


  """
  gemini 라이브러리 자체로 임베딩 
  """
  # @classmethod
  # def geminiEmbedding(cls,contentList):
  #   embeddingModel = current_app.config['embeddingModel']
  #
  #   embeddingResult = []
  #
  #   for text in contentList:
  #     #gemini한테 임베딩 요청
  #     result = genai.embed_content(
  #         model=embeddingModel,
  #         content=text
  #     )
  #     embeddingResult.append(result['embedding'])
  #
  #   return embeddingResult

  # 랭체인을 이용한 gemini 임베딩
  @classmethod
  def geminiEmbedding(cls,contentList):
    embeddingModel = current_app.config['embeddings']

    embeddingsResult = embeddingModel.embed_documents(contentList)

    return embeddingsResult

  """
  Gemini Api서버에 파일 업로드
  """
  def uploadToGemini(self,path, mime_type=None):
      file = genai.upload_file(path, mime_type=mime_type)
      while file.state.name == "PROCESSING":
        current_app.logger.info('Waiting for video to be processed.')
        time.sleep(10)
        file = genai.get_file(file.name)

      if file.state.name != "ACTIVE":
        raise Exception(f"File {file.name} upload failed to process")

      current_app.logger.info(f'{file.name} upload successful')

      return file

  def createResponseSchema(self,dicFieldList):
    dicFieldList.append("타임코드")
    dicFieldList.append("시작시간")
    dicFieldList.append("종료시간")
    # videoAnalysis의 내부 딕셔너리를 위한 TypedDict 동적 생성
    interiorDicInfo = typing.cast(
        typing.Type[typing.TypedDict],
        types.new_class("ResultDict", (typing.TypedDict,), {},
                        lambda ns: ns.update({key: str for key in dicFieldList} | {"__annotations__": {key: str for key in dicFieldList}}))
    )
    # 외부 딕셔너리(최종 결과)를 위한 TypedDict 정의
    class ResultDict(typing.TypedDict):
      videoAnalysis: typing.List[interiorDicInfo]

    # print("필드 리스트=>", list(interiorDicInfo.__annotations__.keys()))

    return ResultDict




