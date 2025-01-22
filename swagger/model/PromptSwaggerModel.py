from flask_restx import fields

# PromptSave Api
promptSave = {"title": "Prompt_save_Request", "explanation": {
                          "prompt": fields.String(
                                                   description="생성할 프롬프트 입력",
                                                   required=True,
                                                   example="모범택시 영상인데 이 영상을 3~10초 단위로 분석해줘")
                          }
            }
