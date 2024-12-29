from flask import Flask, jsonify,Blueprint,request,current_app
import os,json
from service.FileService import FileService


# Blueprint 정의
fileController = Blueprint('FileController', __name__)

segmentSaveDir = "./static/video/segments"
os.makedirs(segmentSaveDir, exist_ok=True) #디렉토리 생성(이미 존재하면 패스)
segment_duration = 300 #분할 영상 길이 단위

fileService = FileService()

@fileController.route('/video/split',methods=['POST'])
def videoSplit():
  videoFile = request.files['video']
  save_path = os.path.join( "./static/video/original", videoFile.filename)  # 저장 경로
  originalFilename = os.path.splitext(videoFile.filename)[0]

  # 원본 파일 저장
  videoFile.save(save_path)


  segments = fileService.videoSplit(save_path, originalFilename, segmentSaveDir, segment_duration)


  response = {
    "message": "Video split successfully!",
    "segments": segments
  }

  return jsonify(response)


@fileController.route('/video/merge',methods=['POST'])
def videoMerge():
  videodatas = request.get_json().get("searchResult")

  fileService.videoMerge(videodatas)


  return "ok"


