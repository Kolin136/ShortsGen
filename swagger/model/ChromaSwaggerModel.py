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
                              "searchText": fields.String(
                                  description="시나리오 검색할 글",
                                  required=True,
                                  example="김도기가 박양진한테 보너스 말고 다른 부서로 이동을 부탁하는 장면이고 인물은 김도기,박영진 나와."),
                             }
                }

# ChromaDelete Api
ChromaDelete = {"title": "Chroma_delete_Request", "explanation": {
                              "collectionName": fields.String(
                                  description="백터 DB에 삭제할 컬렉션 이름",
                                  required=True,
                                  example="Mobeomtaeksi")}
               }
