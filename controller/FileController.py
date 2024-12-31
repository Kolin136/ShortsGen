from flask import Flask, jsonify,Blueprint,request,current_app
import os,json
from service.FileService import FileService
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from swagger.parser.FileParsers import *
from swagger.model.FileSwaggerModel import *

# 네임스페이스
fileNamespace = Namespace('1.FileController',description='FileController api 목록')
# Blueprint 정의
# fileController = Blueprint('FileController', __name__)

originalSaveDir = "./static/video/original"
segmentSaveDir = "./static/video/segments"
mergeSaveDir = "./static/video/merge"
os.makedirs(segmentSaveDir, exist_ok=True) #디렉토리 생성(이미 존재하면 패스)
os.makedirs(originalSaveDir, exist_ok=True)
os.makedirs(mergeSaveDir, exist_ok=True)
segment_duration = 300 #분할 영상 길이 단위

fileService = FileService()

@fileNamespace.route('/split')
class videoSplit(Resource):
  @fileNamespace.expect(videoSplitParser)
  @fileNamespace.doc(description="업로드한 비디오를 분리 합니다")
  def post(self):
    """업로드한 비디오를 설정한 단위로 분리하는 API"""
    args = videoSplitParser.parse_args() # 파서로 args 가져오기
    videoFile = args['video']
    save_path = os.path.join( "./static/video/original", videoFile.filename)  # 저장 경로
    originalFilename = os.path.splitext(videoFile.filename)[0]

    # 원본 파일 저장
    videoFile.save(save_path)

    # segments = fileService.videoSplit(save_path, originalFilename, segmentSaveDir, segment_duration)

    response = {
      "message": "Video split successfully!",
      "splitVideos": "gg"
    }

    return jsonify(response)


@fileNamespace.route('/merge')
class videoMerge(Resource):
  @fileNamespace.expect(fileNamespace.model(videoMerge["title"], videoMerge["explanation"]))
  @fileNamespace.doc(description="요청 데이터 분석후 비디오 각 구간 잘라내고 결합후 새비디오 생성 합니다")
  def post(self):
    videodatas = request.get_json().get("searchResult")

    fileService.videoMerge(videodatas)

    return "비디오 생성 성공"


