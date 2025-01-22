from model.PromptModel import Prompt
from repository.SqlAlchemyRepository import SqlAlchemyRepository


sqlAlchemyRepository = SqlAlchemyRepository()

class PromptService:
  def promptSave(self,prompt):
    promptModel = Prompt(
        prompt_text= prompt
    )

    sqlAlchemyRepository.saveOne(promptModel)

