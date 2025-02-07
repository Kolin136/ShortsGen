# Shorts Boost
![Image](https://github.com/user-attachments/assets/932136e1-f140-4986-93e8-03cb77818919)

+ 이 프로젝트는 AI 기반 쇼츠 비디오 자동 생성 서비스입니다.
사용자는 원본 영상을 업로드한 후, AI가 원본 영상을 분석하고 사용자가 원하는 하이라이트 장면을 추출해 영상으로 편집해 줍니다.
이를 통해 불필요한 부분을 제거하고, 유튜브 쇼츠, 틱톡등과 비슷한 짧은 영상을 제작할 수 있습니다.

+ 개발기간 2024.12 ~2025.02
  
# 기술 스택
<div align=center> 
 <img src="https://img.shields.io/badge/googlegemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white">
 <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
 <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
 <img src="https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white">
 <img src="https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white">
  <br>

 <img src="https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white">
 <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
 <img src="https://img.shields.io/badge/redis-FF4438?style=for-the-badge&logo=redis&logoColor=white">
 <img src="https://img.shields.io/badge/swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=white">
 <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <br>
  
 <img src="https://img.shields.io/badge/ffmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white">
 <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
 <img src="https://img.shields.io/badge/css-663399?style=for-the-badge&logo=css&logoColor=white">
 <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
  <br>
</div>

# 설치,환경 셋팅 방법
### 1. 프로젝트 원하는 위치에 클론 후, 프로젝트 경로로 이동하고 가상환경 생성, 활성화하고 필요한 패키지 등을 다운로드합니다.

    ```bash
    # 가상환경 생성
    python3 -m venv .venv
    ```

    ```bash
    # 가상환경 활성화
    source .venv/bin/activate  # Mac의 경우
    .venv\Scripts\activate     # Windows의 경우
    ```

    ```bash
    # pipList.txt에 적힌 패키지 설치
    pip install -r pipList.txt
    ```

### 2. ffmpeg 패키지 설치

    **Mac의 경우**
    ```bash
    brew install ffmpeg
    ```

    **Windows의 경우**  
    [참고해서 설치](https://kolin136.tistory.com/174)

### 3. Redis 설치,서버실행

    **Mac의 경우**
    ```bash
    brew install redis
    redis-server
    #재부팅 후에도 자동 실행 할 경우에는 이 방법으로
    brew services start redis 
    ```
    **Windows의 경우는 구글에서 Redis 설치,실행방법 검색하면 많이 나옵니다**

### 4. DB, 환경변수 파일 세팅

    ```sql
    # "shorts_boost" 데이터베이스 생성
    CREATE DATABASE shorts_boost;
    ```

    ```bash
    # 테이블 생성
    python createTables.py
    ```

    프로젝트의 최상단에 .env 파일 생성후 값 입력
    (GEMINI_API_KEY는 [공식사이트](https://aistudio.google.com/welcome) 에서 API_KEY 발급 받으세요)
    ```bash
    GEMINI_API_KEY= 
    DB_NAME=shorts_boost
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    
    #Chroma
    CHROMA_DIRECTORY="./vectorstorage/chroma"
    
    #Cleary (BROKER_URL랑 CELERY_RESULT_BACKEND 동일하게)
    BROKER_URL= 
    CELERY_RESULT_BACKEND= 
    ```
    







    
