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

  ```bash
    # 프로젝트 경로 말고,맥 경로에서
    brew install ffmpeg # 맥의 경우
  ```

  **Windows의 경우**  
  [참고해서 설치](https://kolin136.tistory.com/174)

### 3. Redis 설치,서버실행

  ```bash
    #Mac의 경우 (프로젝트 경로말고,맥 경로에서)
    brew install redis
    redis-server
    #재부팅 후에도 자동 실행 할 경우에는 이 방법으로
    brew services start redis 
  ```
  #Windows의 경우는 구글에서 Redis 설치,실행방법 검색하면 많이 나옵니다**

### 4. DB, 환경변수 파일 세팅

  ```bash
   사용하는 DB에서 "shorts_boost" 데이터베이스 생성
  ```
  만약 Mysql말고 다른 DB 사용시 [공식문서](https://docs.sqlalchemy.org/en/20/core/engines.html)참고해서 common-config-Config.py코드에서 이 부분 변경 하세요.
  <table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/0ac7ad1a-a0e8-43b5-a17c-b96a5a10e878" width="100%"></td>
  </tr>
  </table>
 

  ```bash
    # 테이블 생성
    python createTables.py
  ```

  ```python
    프로젝트의 최상단에 .env 파일 생성후 값 입력
    (GEMINI_API_KEY는 [공식사이트](https://aistudio.google.com/welcome) 에서 API_KEY 발급 받으세요)
  
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

# 프로젝트 서비스 사용 방법

  ```bash
    #1) 워커 실행
    celery -A celeryApp.celery worker --loglevel=debug --pool=solo
    #2) 서버 실행
    python app.py
  ```


### 1. 비디오 업로드 및 프롬프트 작성

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/376b1c1f-5909-43c1-abc3-7c28fdd75c17" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/2c92e3ae-2da8-447c-90aa-6756ac2ae522" width="100%"></td>
  </tr>
  <tr>
    <td align="center"><b>1. 원하는 비디오 선택 후 업로드 버튼 클릭</b></td>
    <td align="center"><b>2. 비디오 분리 완료 후 스크롤 내린 뒤 프롬프트 제목, 내용 적고 저장</b></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/3a2a19c7-948a-4542-89c1-fd85a2cb5e26" width="50%"></td>
  </tr>
  <tr>
    <td align="center"><b>3. 클릭하면 생성한 프롬프트 조회, 수정, 삭제 가능</b></td>
  </tr>
</table>

## 2. 프롬프트 조회 및 캡셔닝 설정

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/1b1dec2b-f228-4ab2-a8a5-eb52c43647d0" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/e17d297b-ff7f-41c0-871b-9b2d30f61bd9" width="100%"></td>
  </tr>
  <tr>
    <td align="center"><b>1. 캡셔닝 페이지로 이동 후, 분리된 비디오, 프롬프트 선택</b></td>
    <td align="center"><b>2. 캡셔닝시 응답받을 필드 작성,등장인물 정확도 향상 이미지 추가(선택사항)</b></td>
  </tr>
</table>

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/af2dbf3f-0f53-48a5-836e-17b7d29837b7" width="50%"></td>
  </tr>
  <tr>
    <td align="center"><b>3. 캡셔닝 시작 버튼 클릭후 결과-저장 버튼 나오는데,결과 확인후 마음에 들면 저장 버튼 클릭<br>
                             만약 프롬프트 수정후 다시 해당 비디오-프롬프트 기준으로 캡셔닝시 이전 캡셔닝 버튼 클릭하면 이전 캡셔닝 결과랑 비교 가능</b></td>
  </tr>
</table>

## 3. 원하는 장면 검색후 쇼츠 생성하기

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/57ce6e45-7725-4227-8fb8-787c94f542a6" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/903ca2e4-5081-41f8-a5ea-618e45998a4c"  width="100%"></td>
  </tr>
  <tr>
    <td align="center"><b>1. 프롬프트 기준 캡셔닝 완료한 데이터 선택하고,캡셔닝 데이터 저장할 공간 이름 작성후 저장 클릭</b></td>
    <td align="center"><b>2. 저장공간 입력했던값,쇼츠 생성할 장면 내용,쇼츠 제목 입력후 생성 클릭</b></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/639ea4fc-def1-4906-9791-38a94440cd41" width="50%"></td>
  </tr>
  <tr>
    <td align="center"><b>추가) 쇼츠 생성후 또 해당 원본 영상에서 다른 장면 쇼츠 생성 하고 싶을시,저장 공간 이름 생각 안나면 <br>
                         현재 페이지 상단 프롬프트 선택하는 곳에서 프롬프트 클릭 후 컬렉션 보기 클릭 시 확인 가능 </b></td>
  </tr>
</table>

## 4. 생성한 쇼츠 결과 보기
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/b5770c59-f010-4674-9eec-b9f4a9c93790" width="100%"></td>
    <td><img src="https://github.com/user-attachments/assets/d327be1a-d600-49b1-b1ef-95466b585646"  width="100%"></td>
  </tr>
  <tr>
    <td align="center"><b>1. 지금까지 생성한 쇼츠 목록 화면</b></td>
    <td align="center"><b>2. 썸네일 or Watch 버튼 클릭시 재생</b></td>
  </tr>
</table>




    
