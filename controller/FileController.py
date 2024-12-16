from flask import Flask, jsonify, Config
import os,json

from service.FileService import FileService

app = Flask(__name__)
app.config.from_object(Config)  # 설정 파일 적용
output_dir = "../static/segments"
os.makedirs(output_dir, exist_ok=True)
segment_duration = 300 #분할 영상 길이 단위

fileService = FileService()

@app.route('/test_split')
def test_split():
  video_path = r"C:\Users\jsowb\Desktop\gate.mp4"


  segments = fileService.fileSplit(video_path, output_dir, segment_duration)

  response = {
    "message": "Video split successfully!",
    "segments": segments
  }
  # JSON 데이터를 보기 좋게 포매팅
  formatted_response = json.dumps(response, ensure_ascii=False, indent=4)

  return app.response_class(
      response=formatted_response,
      status=200,
      mimetype="application/json"
  )

if __name__ == '__main__':
  app.run(debug=True)


# 영상 업로드 및 분리 엔드포인트
# @app.route('/upload', methods=['POST'])
# def upload_video():
#   # 사용자가 업로드한 파일 받아오기
#   video_file = request.files['video']
#   segment_duration = int(request.form.get('segment_duration', 60))  # 원하는 분리 길이 (초)
#
#   # 저장 경로 설정
#   upload_path = f"./uploads/{video_file.filename}"
#   output_dir = "./segments"
#   os.makedirs(output_dir, exist_ok=True)  # 분리된 영상 저장 디렉토리 생성
#
#   # 파일 저장
#   video_file.save(upload_path)
#
#   # 영상 분리 및 저장
#   segments = split_video_with_intervals(upload_path, output_dir, segment_duration)
#
#   # 반환
#   return jsonify({"message": "Video split successfully!", "segments": segments})


