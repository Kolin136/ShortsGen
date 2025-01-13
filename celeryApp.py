import os
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.Config import DevelopmentConfig
from dotenv import load_dotenv

# include는 Celery 작업(Task)이 정의된 파일 이름적고 만약 하위 디렉토리에 있다면 myapp.tasks.controllertest 이런식으로 적는다
celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0',include=['controller.FileController'])

# Flask 애플리케이션 팩토리 함수
load_dotenv()

celeryDb = SQLAlchemy()

def create_celery_app():
  flask_app = Flask(__name__)
  flask_app.config.from_object(DevelopmentConfig)

  # SQLAlchemy 초기화
  celeryDb.init_app(flask_app)
  flask_app.config['celeryDb'] = celeryDb

  return flask_app

# Flask 애플리케이션 생성 및 Celery 설정
flask_app = create_celery_app()
celery.conf.update(flask_app.config)

# ContextTask 설정 (Flask 애플리케이션 컨텍스트 활성화)
# __call__은 파이썬에서 클래스의 객체가 함수처럼 호출될 때 실행되는 특별한 메소드이고 여기서  __call__는 Celery 작업이 실행될 때 실행되는 메소드를 오버라이드 하는거다
class ContextTask(celery.Task):
  def __call__(self, *args, **kwargs):
    with flask_app.app_context(): # Flask 앱 컨텍스트 활성화
      return self.run(*args, **kwargs)

# Celery의 기본 작업 클래스(celery.Task)를  위에서 만든 커스텀 클래스인 ContextTask로 교체하는 코드
# 이제 모든 Celery 작업이 ContextTask를 기반으로 동작하며, Flask 앱 컨텍스트 내에서 실행
celery.Task = ContextTask