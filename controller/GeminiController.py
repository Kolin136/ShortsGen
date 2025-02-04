import os
from flask import Blueprint, jsonify ,request, render_template
from flask import current_app

from common.exception.GlobalException import CustomException
from service.GeminiService import GeminiService
import json
from flask_restx import Namespace, Resource
from swagger.parser.GeminiParsers import *
from swagger.model.GeminiSwaggerModel import *
from flask import make_response


# 네임스페이스
geminiNamespace = Namespace('2.GeminiController',description='GeminiController api 목록')

geminiService = GeminiService()

@geminiNamespace.route('/captioning')
class geminiVideoCaptioning(Resource):
  @geminiNamespace.expect(geminiVideoCaptioningParser)
  @geminiNamespace.doc(description="업로드한 비디오를 캡셔닝 합니다")
  def post(self):
    """비디오 캡셔닝 API"""
    # 전역으로 모델 초기화한거 가져오기
    geminiModel = current_app.config['model']
    args = geminiVideoCaptioningParser.parse_args() # 파서로 args 가져오기
    # 요청에서 JSON,이미지 데이터 가져오기
    imagesList = args["images"]
    try:
      splitVideoList = json.loads(args["splitVideos"])["splitVideos"]
      userPrompt = args["prompt"]
      promptId = args["promptId"]
      jsonFieldList = [field.strip() for field in args["jsonFieldList"].split(",")]
    except Exception as e:
      raise CustomException("선택사항 제외 모든 필드 다 입력해 주세요", str(e), 400)

    result = geminiService.videoCaptioning(geminiModel,splitVideoList,imagesList,promptId,userPrompt,jsonFieldList)

    response = {
      "videoAnalysis": result
    }

    return response

@geminiNamespace.route('/save')
class geminiCaptioningSave(Resource):
  @geminiNamespace.expect(geminiNamespace.model(geminiCaptioningSave["title"], geminiCaptioningSave["explanation"]))
  @geminiNamespace.doc(description="캡셔닝 데이터 저장 합니다")
  def post(self):
    """캡셔닝 데이터 일반 DB저장 API"""
    try:
      videoAnalysisData =request.get_json().get("videoAnalysis")
    except Exception as e:
      raise CustomException("캡셔닝 응답 Json이 없습니다. 캡셔닝 부터 해주세요", str(e), 400)

    geminiService.geminiCaptioningSave(videoAnalysisData)

    return "캡셔닝 데이터 DB 저장 성공"

@geminiNamespace.route('/captioning/video/<video_id>/prompt/<prompt_id>')
class geminiCaptioningSearch(Resource):
  @geminiNamespace.doc(description="특정 캡셔닝 데이터들 조회 합니다")
  def get(self,video_id,prompt_id):
    """특정 캡셔닝 데이터 조회 API"""
    #패스 파라미터값 가져오기
    videoId = video_id
    promptId = prompt_id

    result = geminiService.geminiCaptioningSearch(videoId,promptId)

    response = {
      "videoAnalysis": result
    }

    return response


@geminiNamespace.route('/captioning/prompt/<prompt_id>')
class geminiCaptioningSearchCollectionName(Resource):
  @geminiNamespace.doc(description="특정 캡셔닝 데이터에서 벡터DB 컬렉션 이름 조회")
  def get(self,prompt_id):
    """특정 캡셔닝 데이터에서 벡터DB 컬렉션 이름 조회 API"""
    #패스 파라미터값 가져오기
    promptId = prompt_id

    result = geminiService.geminiCaptioningSearchCollectionName(promptId)

    response = {
      "collectionName": result
    }

    return response