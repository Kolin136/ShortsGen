import os

from flask import Blueprint, jsonify ,request, render_template
from flask import current_app
from service.GeminiService import GeminiService
import json

# Blueprint 정의
geminiController = Blueprint('geminiController', __name__)

geminiService = GeminiService()

@geminiController.route('/gemini/captioning',methods=['POST'])
def geminiVideoCaptioning():
  # 전역으로 모델 초기화한거 가져오기
  gemini_llm = current_app.config['model']

  # 요청에서 JSON,이미지 데이터 가져오기
  segmentList = json.loads(request.form.get("segments"))['segments']
  imagesList = request.files.getlist('images')
  videoTitle = request.form.get("videoTitle")
  videoLength = request.form.get("videoLength")

  result = geminiService.videoCaptioning(gemini_llm,segmentList,imagesList,videoTitle,videoLength)

  response = {
    "videoAnalysis": result
  }

  return jsonify(response)


@geminiController.route('/gemini/save',methods=['POST'])
def geminiCaptioningSave():
  videoAnalysisData =request.get_json().get("videoAnalysis",[])

  geminiService.geminiCaptioningSave(videoAnalysisData)

  return "영상분석 결과 DB 저장 성공"


