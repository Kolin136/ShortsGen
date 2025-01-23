from flask_restx import fields
import json
# geminiCaptioningSave Api
CaptioningExample = [
  {
    "promptId": "1",
    "videoId": 8,
    "videoName": "company_0_56.mp4",
    "대사": "무슨 점수?",
    "등장인물": "박양진",
    "시작시간": "00:12",
    "요약": "박양진이 무슨 점수냐고 묻는다.",
    "종료시간": "00:12",
    "타임코드": "00:12~00:12"
  },
  {
    "promptId": "1",
    "videoId": 8,
    "videoName": "company_0_56.mp4",
    "대사": "인사 고과 점수요.",
    "등장인물": "김도기",
    "시작시간": "00:12",
    "요약": "김도기가 인사 고과 점수라고 말한다.",
    "종료시간": "00:14",
    "타임코드": "00:12~00:14"
  }
]
# JSON 형식으로 포맷팅된 문자열 생성
formattedCaptioningExample = json.dumps(CaptioningExample, indent=2, ensure_ascii=False)
geminiCaptioningSave = {"title": "Gemini_captioning_save_Request", "explanation": {
                              "videoAnalysis": fields.List(fields.String,
                              description="Gemini 캡셔닝 API 응답 'videoAnalysis'필드값 데이터 넣어 주세요",
                              example=formattedCaptioningExample, required=True)}
                      }