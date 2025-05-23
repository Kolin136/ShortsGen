import os
import time
from flask import current_app
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re
import json
from common.exception.GlobalException import CustomException
from model.VideoCaptioningModel import VideoCaptioning
from prompt.CaptioningPrompt import PromptTemplate
from repository.SqlAlchemyRepository import SqlAlchemyRepository
from repository.VideoCaptioningRepository import VideoCaptioningRepository
from io import BytesIO
import types
import typing_extensions as typing



sqlAlchemyRepository = SqlAlchemyRepository()
videoCaptioningRepository = VideoCaptioningRepository()


class GeminiService:
  """
  비디오 캡셔닝 작업 
  """
  def videoCaptioning(self,geminiModel,splitVideoList,imagesList,promptId,userPrompt,jsonFieldList):
    # JSON 데이터 검증
    if not splitVideoList:
      raise CustomException("비디오가 제공되지 않았습니다.", statusCode=400)

    # 'segments' 폴더에서 파일 찾기
    segmentsFolder = os.path.normpath("./static/video/segments")  # 경로 표준화
    filesToProcess = []

    for segment in splitVideoList:
      videoPath = os.path.normpath(os.path.join(segmentsFolder, segment["videoName"])) # OS에 맞는 경로 조합
      if os.path.exists(videoPath):
        filesToProcess.append(videoPath)
      else:
        raise CustomException({"error": f"파일 '{segment['videoName']}'을 찾을 수 없습니다."},statusCode=404)

    # chat_session = geminiModel.start_chat(history=[])
    result = []

    promptList = []  #프롬프트에 업로드한 영상,이미지 포함시키기 위해서
    #영상 업로드 작업
    for file_path in filesToProcess:
      try:
        uploadVideo = self.uploadToGemini(file_path, mime_type="video/mp4")
        promptList.append(uploadVideo)
      except Exception as e:
        raise CustomException("Gemini 서버 비디오 업로드 실패",str(e),statusCode=500)  # 500 Internal Server Error

    # 이미지 업로드 작업
    characters = []
    if imagesList and all(image.filename for image in imagesList):
      for image in imagesList:
        # BytesIO로 변환
        imageByteStream = BytesIO(image.read())
        imageByteStream.seek(0)
        try:
          uploadImage = self.uploadToGemini(imageByteStream, mime_type=image.mimetype)
          promptList.append(uploadImage)
        except Exception as e:
          raise CustomException("Gemini 서버 이미지 업로드 실패",str(e),statusCode=500)

        characters.append(os.path.splitext(image.filename)[0]) # 확장자 제거)

    prompt = PromptTemplate.prompt(characters,userPrompt)
    promptList.append(prompt)

    #LLM 응답 Json형식 설정
    ResultDict = self.createResponseSchema(jsonFieldList)

    # response = chat_session.send_message(promptList) #gemini한테 요청 보내는 메소드(히스토리 자동관리 방식)
    response = geminiModel.generate_content(promptList, generation_config=genai.GenerationConfig(temperature=0, response_mime_type="application/json", response_schema=ResultDict))
    current_app.logger.info(f'캡셔닝 결과: {response.text}')
    # LLM 응답받은 문자열을 정규식으로 JSON 리스트 추출
    match = re.search(r'\[\s*{.*?}\s*\]', response.text, re.DOTALL)

    if match:
      jsonListStr = match.group()  # JSON 리스트 부분만 추출
      try:
        jsonList = json.loads(jsonListStr)  # 문자열을 Python 리스트로 변환
        # 각 딕셔너리에 "videoName","videoId","promptId" 키 추가
        for item in jsonList:
          item["videoName"] = splitVideoList[0]["videoName"]  # videoName에 파일 경로 추가
          item["videoId"] = splitVideoList[0]["videoId"]
          item["promptId"] = promptId

        result.extend(jsonList)  # 파싱된 리스트를 결과 리스트에 추가
      except json.JSONDecodeError:
        raise CustomException({"Gemini 응답 JSON 형식이 잘못되었습니다. 다시 시도해 주세요."},statusCode=500)
    else:
      raise CustomException("Json형식 응답받지 못했거나 Gemini 서버의 중간 오류가 있었습니다. 다시 요청 해주세요",statusCode=500)

    return result

  """
  비디오 캡셔닝 결과 DB에 저장 메소드
  """
  def geminiCaptioningSave(self, videoAnalysisData):
    # 기존 비디오Id,프롬프트Id에 해당하는 캡셔닝 데이터가 이미 DB에 존재하는데, 동일한 비디오ID,캡셔닝ID의 새로운 캡셔닝 결과가 마음에 드는경우
    # 저장하면 중복으로 저장하므로 이전 해당 캡셔닝 데이터들 삭제후 저장하도록 한다.
    videoId = videoAnalysisData[0]["videoId"]
    promptId = videoAnalysisData[0]["promptId"]
    videoCaptioningRepository.deleteByVideoIdAndPromptId(videoId, promptId)

    VideoCaptioningList = []
    for jsonData in videoAnalysisData:
        # VideoCaptioningModel 객체 생성 및 매핑
        VideoCaptioningList.append(VideoCaptioning(
            video_id=int(jsonData["videoId"]),
            prompt_id=int(jsonData["promptId"]),
            video_analysis_json=jsonData,
            timecode=jsonData["타임코드"],
            start_time=jsonData["시작시간"],
            end_time=jsonData["종료시간"])
        )

    sqlAlchemyRepository.saveAll(VideoCaptioningList)


  def geminiCaptioningSearch(self, videoId, promptId):
    videoCaptioningModelList = videoCaptioningRepository.findByVideoIdAndPromptId(videoId, promptId)
    result= []
    for videoCaptioningModel in videoCaptioningModelList:
      result.append(videoCaptioningModel.video_analysis_json)

    return result


  def geminiCaptioningSearchCollectionName(self, promptId):
    videoCaptioningModel = videoCaptioningRepository.findChromaCollectionByPromptId(promptId)
    if videoCaptioningModel is None:
      raise CustomException("해당 캡셔닝 데이터에 컬렉션 이름이 존재하지 않습니다.",statusCode=404)

    return str(videoCaptioningModel.chroma_collection_name)




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
        current_app.logger.info('비디오 업로드 처리를 기다리는 중')
        time.sleep(10)
        file = genai.get_file(file.name)

      if file.state.name != "ACTIVE":
        raise Exception(f"File {file.name} upload failed to process")

      current_app.logger.info(f'{file.name} 업로드 성공')

      return file

  """
  Gemini에서 지원하는 출력형식 지정 설정
  """
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

  @classmethod
  def generalSingletonQuestions(self,prompt):
    geminiModel = current_app.config['model']
    # 프롬프트에 욕설,괴롭힘,혐오 표현이 있어도 차단 안하고 응답하도록 하는 설정
    safetySettings = {
      HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    response = geminiModel.generate_content([prompt],safety_settings=safetySettings)
    return response.text





