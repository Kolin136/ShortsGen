from flask import request
from flask_restx import Namespace, Resource
from swagger.model.PromptSwaggerModel import *
from service.PromptService import PromptService

# 네임스페이스
promptNamespace = Namespace('4.PromptController',description='PromptController api 목록')

promptService = PromptService()

@promptNamespace.route('/save')
class PromptSave(Resource):
  @promptNamespace.expect(promptNamespace.model(promptSave["title"], promptSave["explanation"]))
  @promptNamespace.doc(description="프롬프트 저장 합니다")
  def post(self):
    """프롬프트 저장"""
    prompt = request.get_json().get("prompt")

    promptService.promptSave(prompt)

    return "프롬프트 저장 완료"