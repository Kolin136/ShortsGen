from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

class SqlAlchemyRepository:

  def saveOne(self,data):
    g.db.session.add(data)
    g.db.session.commit()

  def saveAll(self,dataList):
    for data in dataList:
      g.db.session.add(data)
    g.db.session.commit()

  def celerySaveAll(self,dataList):
    db = current_app.config['celeryDb']
    for data in dataList:
      db.session.add(data)
    db.session.commit()