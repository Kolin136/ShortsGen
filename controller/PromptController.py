from flask import request
from flask_restx import Namespace, Resource

from common.exception.GlobalException import CustomException
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
    try:
      title = request.get_json()['title']
      prompt = request.get_json().get("prompt")
    except Exception as e:
      raise CustomException("프롬프트 제목이랑 프롬프트를 입력해 주세요", str(e), 400)

    promptService.promptSave(title,prompt)

    return "프롬프트 저장 완료"

@promptNamespace.route('/search')
class PromptAllSearch(Resource):
  @promptNamespace.doc(description="모든 프롬프트 조회 합니다")
  def get(self):
    """모든 프롬프트 조회"""
    promptList = promptService.promptAllSearch()

    response = {
      "prompts": promptList
    }

    return response

@promptNamespace.route('/search/<prompt_id>')
class PromptSearch(Resource):
  @promptNamespace.doc(description="특정 프롬프트 조회 합니다")
  def get(self,prompt_id):
    """특정 트롬프트 조회"""
    #패스 파라미터값 가져오기
    promptId = prompt_id

    prompt = promptService.promptSearch(promptId)

    response = {
      "prompt": prompt
    }
    return response

@promptNamespace.route('/update')
class PromptUpdate(Resource):
  @promptNamespace.expect(promptNamespace.model(promptUpdate["title"], promptUpdate["explanation"]))
  @promptNamespace.doc(description="프롬프트 수정 합니다")
  def put(self):
    """프롬프트 수정"""
    promptId = request.get_json().get("promptId")
    title = request.get_json().get("updateTitle")
    prompt = request.get_json().get("updatePrompt")

    promptService.promptUpdate(promptId,title,prompt)

    return "프롬프트 수정 완료"

@promptNamespace.route('/delete/<prompt_id>')
class PromptDelete(Resource):
  @promptNamespace.doc(description="프롬프트 삭제 합니다")
  def delete(self,prompt_id):
    """프롬프트 삭제"""
    #패스 파라미터값 가져오기
    promptId = prompt_id

    promptService.promptDelete(promptId)

    return f"{promptId}번 프롬프트 삭제 완료"