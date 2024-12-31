from flask import request, jsonify
import os

from werkzeug.datastructures import FileStorage

from service.FileService import FileService
from flask_restx import Namespace, Resource, fields, reqparse
from swagger.model.FileSwaggerModel import *
# File 네임스페이스
file_namespace = Namespace('File', description='File operations', path='/video')

originalSaveDir = "./static/video/original"
segmentSaveDir = "./static/video/segments"
mergeSaveDir = "./static/video/merge"
os.makedirs(segmentSaveDir, exist_ok=True)
os.makedirs(originalSaveDir, exist_ok=True)
os.makedirs(mergeSaveDir, exist_ok=True)
segment_duration = 300

fileService = FileService()



video_merge_request_model = file_namespace.model('VideoMergeRequest', {
  "videoIdList": fields.List(fields.String,
                             description="비디오 ID 목록",
                             required=True,
                             example=["11", "12", "13"]),
  "collectionName": fields.String(
      description="컬렉션 이름",
      required=True,
      example="Mobeomtaeksi")
}
                                                 )


# /split API 요청 파서 정의
video_split_parser = reqparse.RequestParser()
video_split_parser.add_argument('video', location='files', type=FileStorage, required=True, action='append', help='비디오 파일을 업로드 해야합니다')
video_split_parser.add_argument('name', type=str, location='form', required=True, help='이름을 입력해야 합니다')
video_split_parser.add_argument('email', type=str, location='form', required=True, help='이메일을 입력해야 합니다')


@file_namespace.route('/split')
class VideoSplitResource(Resource):
  @file_namespace.expect(video_split_parser)
  @file_namespace.doc(description="업로드한 비디오를 분리 합니다")
  def post(self):
    """업로드한 비디오를 설정한 단위로 분리하는 API"""
    args = video_split_parser.parse_args() # 파서로 args 가져오기
    videoFile = args['video'] # FileStorage 객체 가져오기
    name = args['name']
    email = args['email']

    # videoFile = request.files['video'] # 이부분 주석 또는 삭제
    save_path = os.path.join(originalSaveDir, videoFile.filename)
    originalFilename = os.path.splitext(videoFile.filename)[0]

    videoFile.save(save_path)
    # segments = fileService.videoSplit(save_path, originalFilename, segmentSaveDir, segment_duration)
    segments = {
      "test": "성공입니다",
      "name": name,
      "email": email
    }
    response = {
      "message": "Video split successfully!",
      "segments": segments
    }

    return response

@file_namespace.route('/merge')
class VideoMergeResource(Resource):
  @file_namespace.expect(video_merge_request_model)
  @file_namespace.doc(description="Merges video segments based on the provided list.")
  @file_namespace.response(200, 'Successfully merged')
  @file_namespace.response(400, 'Validation Error')
  def post(self):
    """Merges video segments based on the provided list."""
    videodatas = request.get_json().get("searchResult")
    fileService.videoMerge(videodatas)
    return 'Successfully merged', 200

# ====================  /echo ============================
# 요청 및 응답 모델 정의 (응답 모델은 Swagger UI 표시에만 사용)
# echo_request_model = file_namespace.model(echoModel['title'], echoModel['explanation'])

@file_namespace.route('/echo')
class EchoResource(Resource):
  # @file_namespace.expect(echo_request_model)
  @file_namespace.doc(description="보낸 게시글 내용 그대로 답변 테스트용입니다")
  @file_namespace.response(200, '하하하')
  @file_namespace.response(400, 'Validation Error')
  def post(self):
    """보낸 게시글 그대로 답변 API"""
    data = request.get_json().get("contents")
    if not data: # 'contents' not in data 이부분 삭제 data값이 없다면으로 변경.
      return {'message': 'Invalid request: contents field is required.'}, 400

    response = {'result': data}

    return response, 200

# ====================  /echo ============================
# 요청 및 응답 모델 정의 (응답 모델은 Swagger UI 표시에만 사용)
# echo_request_model = file_namespace.model('EchoRequest', {
#   'contents': fields.String(description='유저가 값을 입력해야합니다', required=True)
# })
#
# # 응답 모델은 Swagger UI 표시에만 사용
# echo_response_model = file_namespace.model('EchoResponse', {
#   'result': fields.String(description='Echoed content')
# })
#
# @file_namespace.route('/echo')
# class EchoResource(Resource):
#   @file_namespace.expect(echo_request_model)
#   # @file_namespace.marshal_with(echo_response_model)  # 제거
#   @file_namespace.doc(description="Echoes back the user's input.")
#   @file_namespace.response(200, 'Successfully echoed', echo_response_model)
#   @file_namespace.response(400, 'Validation Error')
#   def patch(self):
#     """Echoes back the user's input."""
#     data = request.get_json().get("contents")
#     if not data: # 'contents' not in data 이부분 삭제 data값이 없다면으로 변경.
#       return {'message': 'Invalid request: contents field is required.'}, 400
#
#     response = {'result': data}
#
#     return response, 200