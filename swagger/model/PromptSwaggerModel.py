from flask_restx import fields

# PromptSave Api
promptSave = {"title": "Prompt_Save_Request", "explanation": {
                          "title": fields.String(
                                                  description="생성할 프롬프트 제목 입력",
                                                  required=True,
                                                  example="모범택시 프롬프트"),
                          "prompt": fields.String(
                                                   description="생성할 프롬프트 입력",
                                                   required=True,
                                                   example="모범택시 영상인데 이 영상을 3~10초 단위로 분석해줘")
                          }
            }

# PromptUpdate Api
promptUpdate = {"title": "Prompt_Update_Request", "explanation": {
                          "promptId": fields.String(
                              description="수정할 프롬프트 pk",
                              required=True,
                              example="1"),
                          "updateTitle": fields.String(
                              description="수정할 프롬프트 제목 입력",
                              required=True,
                              example="모범택시 프롬프트"),
                          "updatePrompt": fields.String(
                              description="수정할 프롬프트 입력",
                              required=True,
                              example="모범택시 영상인데 이 영상을 3~10초 단위로 분석하나,한 장면이 10초 넘으면 그 장면 단위로 분석해줘")
                        }
              }
