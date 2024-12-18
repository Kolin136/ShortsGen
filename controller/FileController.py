from flask import Flask, jsonify,Blueprint,request,current_app
import os,json

from service.FileService import FileService

# Blueprint 정의
fileController = Blueprint('FileController', __name__)

segmentSaveDir = "./static/video/segments"
os.makedirs(segmentSaveDir, exist_ok=True) #디렉토리 생성(이미 존재하면 패스)
segment_duration = 10 #분할 영상 길이 단위

fileService = FileService()

@fileController.route('/test_split',methods=['POST'])
def videoSplit():
  videoFile = request.files['video']
  filename = videoFile.filename  # 원본 파일명
  save_path = os.path.join( "./static/video/original", filename)  # 저장 경로

  # 파일 저장
  videoFile.save(save_path)

  segments = fileService.videoSplit(save_path, filename, segmentSaveDir, segment_duration)

  response = {
    "message": "Video split successfully!",
    "segments": segments
  }
  # # JSON 데이터를 보기 좋게 포매팅
  # formatted_response = json.dumps(response, ensure_ascii=False, indent=4)

  return jsonify(response)



