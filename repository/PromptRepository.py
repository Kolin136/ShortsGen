from flask import g
from model.PromptModel import Prompt

class PromptRepository:
  def updatePrompt(self,promptId,prompt):
    g.db.session.query(Prompt).filter(Prompt.id == promptId).update({Prompt.prompt_text: prompt})
    g.db.session.commit()

  def findAll(self):
    return g.db.session.query(Prompt).all()

  def findByPromptId(self, promptId):
    return g.db.session.query(Prompt).filter(Prompt.id == promptId).first()

  def deleteById(self,promptId):
    g.db.session.query(Prompt).filter(Prompt.id == promptId).delete()
    g.db.session.commit()

