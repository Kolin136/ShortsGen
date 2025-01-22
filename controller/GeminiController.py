import os
from flask import Blueprint, jsonify ,request, render_template
from flask import current_app
from service.GeminiService import GeminiService
import json
from flask_restx import Namespace, Resource
from swagger.parser.GeminiParsers import *
from swagger.model.GeminiSwaggerModel import *


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
    splitVideoList = json.loads(args["splitVideos"])["splitVideos"]
    imagesList = args["images"]
    userPrompt = args["prompt"]
    jsonFieldList = [field.strip() for field in args["jsonFieldList"].split(",")]

    result = geminiService.videoCaptioning(geminiModel,splitVideoList,imagesList,userPrompt,jsonFieldList)

    response = {
      "videoAnalysis": result
    }

    return jsonify(response)

@geminiNamespace.route('/save')
class geminiCaptioningSave(Resource):
  @geminiNamespace.expect(geminiNamespace.model(geminiCaptioningSave["title"], geminiCaptioningSave["explanation"]))
  @geminiNamespace.doc(description="캡셔닝 데이터 저장 합니다")
  def post(self):
    """캡셔닝 데이터 일반 DB저장 API"""
    videoAnalysisData =request.get_json().get("videoAnalysis")

    geminiService.geminiCaptioningSave(videoAnalysisData)

    return "캡셔닝 데이터 DB 저장 성공"


