from model.PromptModel import Prompt
from repository.PromptRepository import PromptRepository
from repository.SqlAlchemyRepository import SqlAlchemyRepository


sqlAlchemyRepository = SqlAlchemyRepository()
promptRepository = PromptRepository()

class PromptService:
  def promptSave(self,prompt):
    promptModel = Prompt(
        prompt_text= prompt
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
           "created_at": str(promptModel.created_at),
           "updated_at": str(promptModel.updated_at),
          }
      )

    return result

  def promptSearch(self, promptId):
    promptModel = promptRepository.findByPromptId(promptId)

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




