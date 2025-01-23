from flask import current_app
from app import create_app, db
from model import VideoCaptioningModel,VideoModel,PromptModel

app = create_app()

with app.app_context():
  db.create_all()
  current_app.logger.info("Tables created successfully!")
