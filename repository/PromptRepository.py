from flask import g
from model.PromptModel import Prompt

class PromptRepository:
  def updatePrompt(self,promptId,prompt):
    g.db.session.query(Prompt).filter(Prompt.id == promptId).update({Prompt.prompt_text: prompt})
    g.db.session.commit()