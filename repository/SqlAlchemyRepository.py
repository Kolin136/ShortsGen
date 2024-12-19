from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

class SqlAlchemyRepository:
  def saveAll(self, dataList):

    for data in dataList:
      g.db.session.add(data)
    g.db.session.commit()