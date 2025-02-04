from flask import request,url_for, send_file, Response, stream_with_context
import os,json

from common.exception.GlobalException import CustomException
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
thumbnailSaveDir = "./static/image/thumbnail"
os.makedirs(segmentSaveDir, exist_ok=True) #디렉토리 생성(이미 존재하면 패스)
os.makedirs(originalSaveDir, exist_ok=True)
os.makedirs(mergeSaveDir, exist_ok=True)
os.makedirs(thumbnailSaveDir, exist_ok=True)

segmentDuration = 60 #분할 영상 길이 단위

fileService = FileService()

@fileNamespace.route('/split')
class videoSplit(Resource):
  @fileNamespace.expect(videoSplitParser)
  @fileNamespace.doc(description="업로드한 비디오를 분리 합니다")
  def post(self):
    """업로드한 비디오를 설정한 단위로 분리하는 API"""
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
    "message": "비디오 분리 성공!",
    "splitVideos": segments
  }

@fileNamespace.route('/split/task-status/<task_id>')
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
    try:
      videodatas = request.get_json().get("searchResult")
      createVideoName = request.get_json().get("createVideoName")
    except Exception as e:
      raise CustomException("벡터DB 시나리오 검색 응답 Json이 없습니다.시나리오 검색부터 해주세요", str(e), 400)

    videoAndThumbnailRul = fileService.videoMerge(videodatas,createVideoName)

    response = videoAndThumbnailRul
    response["message"] = "쇼츠 생성 성공"

    return response


@fileNamespace.route('/merge')
class videoOriginal(Resource):
  @fileNamespace.doc(description="생성한 쇼츠 비디오 모두 조회 합니다")
  def get(self):
    """생성한 모든 쇼츠 비디오 목록 조회 API"""
    # static/video/merge 폴더 경로
    mergeVideoFolder = os.path.join(mergeSaveDir)

    #비디오 파일 목록 가져오기
    videoFiles = os.listdir(mergeVideoFolder)

    fileUrlList= []

    # 파일명을 URL로 변환하여 리스트에 추가
    for videoFileName in videoFiles:
      thumbnailFileName = videoFileName.replace("_shorts.mp4", "") + "_thumbnail.jpg"

      fileUrlList.append(
        {
         "video_url": url_for('static', filename=f'video/merge/{videoFileName}', _external=True),
         "thumbnail_url": url_for('static', filename=f'image/thumbnail/{thumbnailFileName}', _external=True)
        }
      )

    response = {
      'file_url': fileUrlList
    }
    return response


@fileNamespace.route('/original')
class videoOriginal(Resource):
  @fileNamespace.doc(description="분리전 모든 원본 비디오 이름 조회 합니다")
  def get(self):
    """모든 원본 비디오 이름 목록 조회 API"""
    # static/video/original 폴더 경로
    originalVideoFolder = os.path.join(originalSaveDir)

    # 파일 목록 가져오기
    files = os.listdir(originalVideoFolder)

    # 비디오 파일만 필터링
    videoFileNames = [os.path.splitext(f)[0] for f in files]

    response = {
      'fileList': videoFileNames
    }
    return response

@fileNamespace.route('/split/<original_video_name>')
class videoSplitSearch(Resource):
  @fileNamespace.doc(description="분리된 특정 비디오 조회 합니다")
  def get(self,original_video_name):
    """분리된 특정 비디오 조회 API"""
    #패스 파라미터값 가져오기
    originalVideoName = original_video_name

    videosInfo = fileService.videoSplitSearch(originalVideoName)

    response = {
      "splitVideos": videosInfo
    }
    return response