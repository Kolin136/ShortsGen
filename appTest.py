import os
from flask import Flask, g
from dotenv import load_dotenv
import google.generativeai as genai
from config.Config import Config, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
import chromadb
from chromadb.config import Settings
from flask_restx import Api

# .env 파일 로드
load_dotenv()

db = SQLAlchemy()

# Generative AI 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Flask 애플리케이션 초기화 함수
def create_app():
  app = Flask(__name__)

  # Config 클래스 적용
  app.config.from_object(DevelopmentConfig)
  Config.init_app(app)
  app.logger.propagate = True

  # SQLAlchemy 초기화
  db.init_app(app)

  # Flask-RESTX 초기화 (Swagger UI 경로 수정)
  api = Api(app, version='1.0', title='My API', description='A simple API', doc='/swagger/')
  app.config['api'] = api

  # gemini 모델 전역 객체 초기화 및 설정
  model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
  app.config['model'] = model

  # 임베딩 모델 전역 초기화 및 설정
  app.config['embeddingModel'] = "models/text-embedding-004"

  # Chroma 인스턴스 전역 설정
  chromaDirectory = os.getenv("CHROMA_DIRECTORY")
  os.makedirs(chromaDirectory, exist_ok=True)
  chromaClient = chromadb.PersistentClient(path=chromaDirectory, settings=Settings(anonymized_telemetry=False))

  @app.before_request
  def before_request():
    g.db = db
    g.chromaClient = chromaClient

  @app.teardown_request
  def teardown_request(exception=None):
    db.session.remove()


  from fileControllerTest import  file_namespace
  api.add_namespace(file_namespace, path='/api')

  # # FileController를 리소스로 등록
  # api.add_resource(FileController, '/api/video', endpoint='video_resource')


  # from controller.GeminiController import gemini_namespace
  # api.add_namespace(gemini_namespace, path='/api/gemini')
  #
  # from controller.ChromaController import chroma_namespace
  # api.add_namespace(chroma_namespace, path='/api/chroma')

  return app

# Flask 애플리케이션 실행
if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)