from flask_restx import fields

# ChromaSave Api
ChromaSave = {"title": "Chroma_save_Request", "explanation": {
                              "videoIdList": fields.List(fields.String,
                                                         description="캡셔닝 완료후 분리된 비디오 PK 목록(video_clip테이블의 video_id컬럼값)",
                                                         required=True,
                                                         example=["11", "12", "13"]),
                              "collectionName": fields.String(
                                                        description="백터 DB에 기존 or 새로 생성할 컬렉션 이름",
                                                        required=True,
                                                        example="Mobeomtaeksi")}
              }

# ChromaSearch Api
ChromaSearch = {"title": "Chroma_search_Request", "explanation": {
                              "collectionName": fields.String(
                                  description="해당 컬렉션에서 검색할 컬렉션 이름",
                                  required=True,
                                  example="Mobeomtaeksi"),
                              "summary": fields.String(
                                  description="생성할 영상 요약 내용",
                                  required=True,
                                  example="김도기가 박양진한테 보너스 말고 다른 부서로 이동을 부탁하는 장면"),

                              "scene": fields.String(
                                  description="생성할 영상에 나오는 대사",
                                  required=True,
                                  example='"김도기:"보너스 말고 점수로 받고 싶어요" 박양진:"뭐 가고 싶은 부서가 있어?" 김도기:"핵심부서에서 일하고 싶어요" 박양진:"이새끼 웃낀놈이네 보너스나 받거라"'),
                              "chracters": fields.String(
                                  description="생성할 영상에 나오는 등장인물",
                                  required=True,
                                  example="박양진,김도기")}
                }
