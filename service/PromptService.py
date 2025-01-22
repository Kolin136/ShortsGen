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

  def promptUpdate(self, promptId, prompt):
    promptRepository.updatePrompt(promptId,prompt)

