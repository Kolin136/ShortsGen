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
  segments  = request.get_json().get("segments",[])
  videoNames = [segment["videoName"] for segment in segments if segment["videoName"]]

  result = geminiService.videoCaptioning(gemini_llm,videoNames)

  response = {
    "videoAnalysis": result
  }

  return jsonify(response)



