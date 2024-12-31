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
load_dotenv()  # .env 파일의 내용을 환경 변수로 로드

db = SQLAlchemy()

# # Generative AI 설정
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Flask 애플리케이션 초기화 함수
def create_app():
  app = Flask(__name__)

  # Config 클래스 적용
  app.config.from_object(DevelopmentConfig)  # 환경에 따라 DevelopmentConfig 적용
  Config.init_app(app)  # 로깅 설정 적용
  # 로그 전달 활성화
  app.logger.propagate = True

  # SQLAlchemy 초기화
  db.init_app(app)

  # Flask-RESTX 초기화 (Swagger UI 경로 수정)
  api = Api(app, version='1.0', title='ShortBoost', description='ShortBoost Api 테스트', doc='/swagger/')
  app.config['api'] = api

  # gemini 모델 전역 객체 초기화 및 설정
  model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

  #랭체인이용시 초기화 방식
  # model = ChatGoogleGenerativeAI(
  #     model="gemini-2.0-flash-exp",
  #     google_api_key=os.getenv("GEMINI_API_KEY")
  # )
  app.config['model'] = model  # 전역 객체를 app.config에 저장

  # 임베딩 모델 전역 초기화 및 설정
  app.config['embeddingModel'] = "models/text-embedding-004"

  # Chroma 인스턴스 전역 설정
  chromaDirectory = os.getenv("CHROMA_DIRECTORY")
  os.makedirs(chromaDirectory, exist_ok=True)
  chromaClient = chromadb.PersistentClient(path=chromaDirectory,settings=Settings(anonymized_telemetry=False))

  @app.before_request
  def before_request():
    # 애플리케이션 컨텍스트 자동 활성화
    g.db = db
    g.chromaClient = chromaClient
  @app.teardown_request
  def teardown_request(exception=None):
    # 요청 종료 후 세션 정리
    db.session.remove()

  # namespace 등록
  from controller.FileController import fileNamespace
  api.add_namespace(fileNamespace, path='/video')

  from controller.GeminiController import  GeminiNamespace
  api.add_namespace(GeminiNamespace, path='/gemini')


  # Blueprints 등록
  # from controller.FileController import fileController
  # app.register_blueprint(fileController, url_prefix='/api')

  # from controller.GeminiController import geminiController
  # app.register_blueprint(geminiController, url_prefix='/api')

  from controller.ChromaController import chromaController
  app.register_blueprint(chromaController, url_prefix='/api')

  return app

# Flask 애플리케이션 실행
if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)