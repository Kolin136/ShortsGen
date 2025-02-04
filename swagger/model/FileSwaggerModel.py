from flask_restx import fields
import json

# videoMerge Api
videoMergeExample = [
  {
    "end_time": "00:17",
    "start_time": "00:15",
    "timecode": "00:15~00:17",
    "video_id": 3
  },
  {
    "end_time": "00:14",
    "start_time": "00:11",
    "timecode": "00:11~00:14",
    "video_id": 8
  }
]
# JSON 형식으로 포맷팅된 문자열 생성
formattedVideoMergeExample = json.dumps(videoMergeExample, indent=2, ensure_ascii=False)
videoMerge = {"title": "video_merge_Request", "explanation": {
                              "searchResult": fields.List(fields.Raw,
                              description="시나리오 검색 API 응답 'segments' 필드값 데이터 넣어 주세요",
                              example=formattedVideoMergeExample, required=True),
                              "createVideoName": fields.String(
                              description="쇼츠 비디오 생성할 이름",
                              required=True,
                              example="김도기가 승급을 요청")
                              }
              }
