import os
from flask import Blueprint, jsonify ,request, render_template
from flask import current_app
from service.GeminiService import GeminiService
import json
from flask_restx import Namespace, Resource
from swagger.parser.GeminiParsers import *
from swagger.model.GeminiSwaggerModel import *


# 네임스페이스
GeminiNamespace = Namespace('2.GeminiController',description='GeminiController api 목록')

# Blueprint 정의
# geminiController = Blueprint('geminiController', __name__)

geminiService = GeminiService()

@GeminiNamespace.route('/captioning')
class GeminiController(Resource):
  @GeminiNamespace.expect(geminiVideoCaptioningParser)
  @GeminiNamespace.doc(description="업로드한 비디오를 캡셔닝 합니다")
  def post(self):
    # 전역으로 모델 초기화한거 가져오기
    gemini_llm = current_app.config['model']
    args = geminiVideoCaptioningParser.parse_args() # 파서로 args 가져오기
    # 요청에서 JSON,이미지 데이터 가져오기
    videoTitle = args["videoTitle"]
    segmentList = json.loads(args["splitVideos"])['segments']
    imagesList = args["images"]
    videoLength = args["videoLength"]
    print("videoTitle=>",videoTitle)
    print("segmentList=>",segmentList)
    print("imagesList=>",imagesList)
    print("videoLength=>",videoLength)


    # result = geminiService.videoCaptioning(gemini_llm,segmentList,imagesList,videoTitle,videoLength)

    response = {
      "videoAnalysis": "하하"
    }

    return jsonify(response)

# @geminiController.route('/gemini/captioning',methods=['POST'])
# def geminiVideoCaptioning():
#   # 전역으로 모델 초기화한거 가져오기
#   gemini_llm = current_app.config['model']
#
#   # 요청에서 JSON,이미지 데이터 가져오기
#   segmentList = json.loads(request.form.get("splitVideos"))['segments']
#   imagesList = request.files.getlist('images')
#   videoTitle = request.form.get("videoTitle")
#   videoLength = request.form.get("videoLength")
#
#   result = geminiService.videoCaptioning(gemini_llm,segmentList,imagesList,videoTitle,videoLength)
#
#   response = {
#     "videoAnalysis": result
#   }
#
#   return jsonify(response)


# @geminiController.route('/gemini/save',methods=['POST'])
# def geminiCaptioningSave():
#   videoAnalysisData =request.get_json().get("videoAnalysis",[])
#
#   geminiService.geminiCaptioningSave(videoAnalysisData)
#
#   return "영상분석 결과 DB 저장 성공"


