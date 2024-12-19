import os
from flask import Flask
from dotenv import load_dotenv
import google.generativeai as genai
from config.Config import Config, DevelopmentConfig
from controller.FileController import fileController
from controller.GeminiController import geminiController
from flask_sqlalchemy import SQLAlchemy



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


# 전역 객체 초기화 및 설정
  model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

  #랭체인이용시 초기화 방식
  # model = ChatGoogleGenerativeAI(
  #     model="gemini-2.0-flash-exp",
  #     google_api_key=os.getenv("GEMINI_API_KEY")
  # )
  app.config['model'] = model  # 전역 객체를 app.config에 저장

  # Blueprints 등록
  app.register_blueprint(fileController, url_prefix='/api')
  app.register_blueprint(geminiController, url_prefix='/api')

  return app

# Flask 애플리케이션 실행
if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)