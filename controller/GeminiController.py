from cachetools import TTLCache
from flask import Blueprint, jsonify ,request, render_template
from flask import current_app
from service.GeminiService import GeminiService

# Blueprint 정의
geminiController = Blueprint('geminiController', __name__)

# 캐시 초기화 (IP별 메모리 저장, 최대 10개 항목, 30분 동안 유지)
history_cache = TTLCache(maxsize=10, ttl=1800)

geminiService = GeminiService()

@geminiController.route('/gemini/captioning',methods=['POST'])
def geminiVideoCaptioning():
  # 전역으로 모델 초기화한거 가져오기
  gemini_llm = current_app.config['model']

  # 요청에서 JSON 데이터 가져오기
  segmentList = request.get_json().get("segments",[])
  videoNames = [segment["videoName"] for segment in segmentList if segment["videoName"]]

  result = geminiService.videoCaptioning(gemini_llm,segmentList)

  response = {
    "videoAnalysis": result
  }

  return jsonify(response)


@geminiController.route('/gemini/save',methods=['POST'])
def geminiCaptioningSave():
  videoAnalysisData =request.get_json().get("videoAnalysis",[])

  geminiService.geminiCaptioningSave(videoAnalysisData)

  return "영상분석 결과 DB 저장 성공"