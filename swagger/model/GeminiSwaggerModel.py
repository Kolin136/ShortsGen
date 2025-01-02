from flask_restx import fields
import json
# geminiCaptioningSave Api
CaptioningExample = [
  {
        "timecode": "00:31-00:34",
        "start_time": 31,
        "end_time": 34,
        "characters": ["박양진","김도기"],
        "scene": "박양진: 그래서 글로 가고 싶다고? 김도기: 예",
        "emotion": "궁금함",
        "action": "박양진이 김도기에게 확인하고 김도기가 긍정하는 모습",
        "scene_description":"박양진이 김도기에게 전략기획실을 가고싶냐고 물어보고 김도기가 긍정하는 장면",
        "summary": "박양진이 김도기에게 확인하는 장면"
    },
    {
        "timecode": "00:34-00:36",
        "start_time": 34,
        "end_time": 36,
        "characters": ["김도기"],
        "scene": "김도기: 보내주시면은 열심히 일하겠습니다.",
        "emotion": "간절함",
        "action": "김도기가 전략기획실 보내주면 열심히 일하겠다는 장면",
        "scene_description": "김도기가 전략기획실 보내주면 열심히 일하겠다고 말하는 장면",
        "summary": "김도기가 전략기획실 보내주면 열심히 일하겠다고 말하는 장면"
    }
]
# JSON 형식으로 포맷팅된 문자열 생성
formattedCaptioningExample = json.dumps(CaptioningExample, indent=2, ensure_ascii=False)
geminiCaptioningSave = {"title": "Gemini_captioning_save_Request", "explanation": {
                              "videoAnalysis": fields.List(fields.String,
                              description="Gemini 캡셔닝 API 응답 'videoAnalysis'필드값 데이터 넣어 주세요",
                              example=formattedCaptioningExample, required=True)}
                      }