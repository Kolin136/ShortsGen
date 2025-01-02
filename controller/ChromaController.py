from flask import Blueprint,jsonify ,request
from flask_restx import Namespace, Resource
from service.ChromaService import ChromaService
from swagger.model.ChromaSwaggerModel import *

# 네임스페이스
chromaNamespace = Namespace('3.ChromaController',description='ChromaController api 목록')

chromaService = ChromaService()

@chromaNamespace.route('/save')
class ChromaSave(Resource):
  @chromaNamespace.expect(chromaNamespace.model(ChromaSave["title"], ChromaSave["explanation"]))
  @chromaNamespace.doc(description="일반 DB에 저장 중인 캡셔닝 데이터 가져다가 임베딩후 벡터 DB에 저장 합니다")
  def post(self):
    """캐셔닝 데이터 벡터 DB 저장 API"""
    videoIdList = request.get_json().get("videoIdList",[])
    collectionName = request.get_json().get("collectionName")

    chromaService.ChromaSave(videoIdList,collectionName)

    return jsonify("크로마 DB 저장 완료")

@chromaNamespace.route('/search')
class ChromaSearch(Resource):
  @chromaNamespace.expect(chromaNamespace.model(ChromaSearch["title"], ChromaSearch["explanation"]))
  @chromaNamespace.doc(description="벡터 DB에서 시나리오 검색 합니다")
  def post(self):
    """벡터DB에서 시나리오 검색 API"""
    # searchText = request.get_json().get("searchText")
    collectionName = request.get_json().get("collectionName")
    summary = request.get_json().get("summary")
    scene = request.get_json().get("scene")
    chracters = request.get_json().get("chracters")

    searchResult = chromaService.ChromaSearch(collectionName,summary,scene,chracters)

    response = {
      "searchResult": searchResult
    }

    return jsonify(response)


@chromaNamespace.route('/delete')
class ChromaDelete(Resource):
  @chromaNamespace.expect(chromaNamespace.model(ChromaDelete["title"], ChromaDelete["explanation"]))
  @chromaNamespace.doc(description="벡터 DB에서 해당 컬렉션 일부 데이터 삭제 합니다")
  def delete(self):
    """벡터DB 해당 컬렉션 일부 데이터 삭제 API"""
    collectionName = request.get_json().get("collectionName")

    chromaService.ChromaDelete(collectionName)

