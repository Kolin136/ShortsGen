from common.exception.GlobalException import CustomException
from model.PromptModel import Prompt
from repository.PromptRepository import PromptRepository
from repository.SqlAlchemyRepository import SqlAlchemyRepository


sqlAlchemyRepository = SqlAlchemyRepository()
promptRepository = PromptRepository()

class PromptService:
  def promptSave(self,title,prompt):
    promptModel = Prompt(
        prompt_text= prompt,
        title=title
    )

    sqlAlchemyRepository.saveOne(promptModel)

  def promptAllSearch(self):
    promptModelList = promptRepository.findAll()
    result = []
    for promptModel in promptModelList:
      result.append(
          {
           "prompt_id": str(promptModel.id),
           "prompt_text": promptModel.prompt_text,
           "prompt_title": promptModel.title,
           "created_at": str(promptModel.created_at),
           "updated_at": str(promptModel.updated_at),
          }
      )

    return result

  def promptSearch(self, promptId):
    promptModel = promptRepository.findByPromptId(promptId)
    if promptModel is None:
      raise CustomException(f"Pk {promptId}번 프롬프트는 존재하지 않습니다.",statusCode=404)

    return {
      "prompt_id": str(promptModel.id),
      "prompt_text": promptModel.prompt_text,
      "created_at": str(promptModel.created_at),
      "updated_at": str(promptModel.updated_at),
    }

  def promptUpdate(self, promptId, prompt):
    promptRepository.updatePrompt(promptId,prompt)

  def promptDelete(self, promptId):
    promptRepository.deleteById(promptId)




