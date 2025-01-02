from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

# geminiVideoCaptioning Api
splitVideosExample ="""
{
  "splitVideos": [
    {
      "videoId": 10,
      "videoName": "[VAP]texi_420_840_0_60.mp4"
    },
    {
      "videoId": 11,
      "videoName": "[VAP]texi_420_840_60_120.mp4"
    }
  ]
}
"""


geminiVideoCaptioningParser = reqparse.RequestParser()
geminiVideoCaptioningParser.add_argument("images", type=FileStorage, location='files', action='append',
                                         help="필수는 아니지만 분석시 인물 정확성을 높이고 싶으면 비디오에 나오는 등장인물 이미지 업로드해 주세요 \n(이미지 파일 이름이 꼭 등장인물 이름이어야 합니다.ex) 김도기.PNG)")
geminiVideoCaptioningParser.add_argument("videoTitle", type=str, location="form", required=True, help="비디오 파일 이름 아닌 제목 입력해 주세요")
geminiVideoCaptioningParser.add_argument("videoLength", type=str, location="form", required=True, help="분리된 비디오 길이 (분)단위로 입력해 주세요")
geminiVideoCaptioningParser.add_argument("splitVideos", type=str, location="form", required=True, help=f"비디오 분리API 응답 데이터 그대로 여기에 입력해 주세요. 예시=>\n{splitVideosExample}")


