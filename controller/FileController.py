from flask import request,url_for, send_file, Response, stream_with_context
import os,json
from service.FileService import FileService
from flask_restx import Namespace, Resource
from swagger.parser.FileParsers import *
from swagger.model.FileSwaggerModel import *
import time
from celeryApp import celery

# 네임스페이스
fileNamespace = Namespace('1.FileController',description='FileController api 목록')

originalSaveDir = "./static/video/original"
segmentSaveDir = "./static/video/segments"
mergeSaveDir = "./static/video/merge"
os.makedirs(segmentSaveDir, exist_ok=True) #디렉토리 생성(이미 존재하면 패스)
os.makedirs(originalSaveDir, exist_ok=True)
os.makedirs(mergeSaveDir, exist_ok=True)
segmentDuration = 300 #분할 영상 길이 단위

fileService = FileService()

@fileNamespace.route('/split')
class videoSplit(Resource):
  @fileNamespace.expect(videoSplitParser)
  @fileNamespace.doc(description="업로드한 비디오를 분리 합니다")
  def post(self):
    """업로드한 비디오를 설정한 단위로 분리하는 API"""
    start_time = time.time()
    args = videoSplitParser.parse_args() # 파서로 args 가져오기
    videoFile = args['video']
    savePath = os.path.join(originalSaveDir, videoFile.filename)  # 저장 경로
    originalFilename = os.path.splitext(videoFile.filename)[0]

    # 원본 파일 저장
    videoFile.save(savePath)

    task = videoSplitBackground.delay(savePath, originalFilename, segmentSaveDir, segmentDuration)

    return {'task_id': task.id}, 202

@celery.task()
def videoSplitBackground(savePath, originalFilename, segmentSaveDir, segmentDuration):

  segments = fileService.videoSplit(savePath, originalFilename, segmentSaveDir, segmentDuration)
  return {
    "message": "Video split successfully!",
    "splitVideos": segments
  }

@fileNamespace.route('/split/task-status/<task_id>', methods=['GET'])
class videoSplitStatus(Resource):
  @fileNamespace.doc(description="업로드한 비디오 분리 Api 호출후 비동기 백그라운드 작업중 완료되었나 확인합니다")
  def get(self, task_id):
    """비디오 분리 비동기 작업 완료 확인(폴링)"""
    task = celery.AsyncResult(task_id)
    if task.state == 'FAILURE':
      return {
        'state': task.state,
        'status': str(task.info),
        'traceback': task.traceback  # 오류 추적 정보
      }, 500
    elif task.state == 'PENDING':
      return {'state': task.state, 'status': '대기 중...'}, 200
    else:
      return {'state': task.state, 'result': task.result}, 200


@fileNamespace.route('/merge')
class videoMerge(Resource):
  @fileNamespace.expect(fileNamespace.model(videoMerge["title"], videoMerge["explanation"]))
  @fileNamespace.doc(description="요청 데이터 분석후 비디오 각 구간 잘라내고 결합후 새비디오 생성 합니다")
  def post(self):
    """새비디오(쇼츠) 생성 API"""
    videodatas = request.get_json().get("searchResult")

    final_video_path = fileService.videoMerge(videodatas)

    # /static 부분을 추가하여 URL 생성
    file_url = url_for('static', filename=final_video_path.replace("./static/", ""), _external=True)

    return {
      "message": "비디오 생성 성공",
      "file_url": file_url
    }

