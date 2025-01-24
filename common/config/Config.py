import logging
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()  # .env 파일에서 환경 변수 가져오기

class Config:
  JSON_AS_ASCII = False
  # 객체들(예: 모델 인스턴스)에 변경이 발생했을 때 이를 추적하고 기록하는거 메모리 많이 잡아먹어서 비활성화
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  @staticmethod
  def init_app(app):
    """애플리케이션 로깅 설정"""

    # 기본 로거 설정
    logging.basicConfig(level=logging.INFO)

    # StreamHandler: 콘솔 출력용 로그
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(stream_handler)


class DevelopmentConfig(Config):
  SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
  )

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@prod-db-host:3306/prod-database"
  )