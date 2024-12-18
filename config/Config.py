import logging
class Config:
  JSON_AS_ASCII = False

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
