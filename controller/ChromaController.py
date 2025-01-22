import os

from flask import Blueprint, jsonify, request, current_app, g
from flask_restx import Namespace, Resource
from service.ChromaService import ChromaService
from swagger.model.ChromaSwaggerModel import *
from langchain_chroma import Chroma

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
    # 랭체인을 이용한 임베딩+벡터DB
    embeddingModel = current_app.config['embeddings']
    vectorStore = Chroma(
        collection_name=collectionName,
        embedding_function=embeddingModel,
        persist_directory=os.getenv("CHROMA_DIRECTORY")
    )

    # chromaService.ChromaSave(videoIdList,collectionName)
    chromaService.ChromaSave(videoIdList,vectorStore,collectionName)

    return "크로마 DB 저장 완료"

@chromaNamespace.route('/search')
class ChromaSearch(Resource):
  @chromaNamespace.expect(chromaNamespace.model(ChromaSearch["title"], ChromaSearch["explanation"]))
  @chromaNamespace.doc(description="벡터 DB에서 시나리오 검색 합니다")
  def post(self):
    """벡터DB에서 시나리오 검색 API"""
    # searchText = request.get_json().get("searchText")
    collectionName = request.get_json().get("collectionName")
    searchText = request.get_json().get("searchText")


    # 랭체인을 이용한 임베딩+벡터DB
    embeddingModel = current_app.config['embeddings']
    vectorStore = Chroma(
        collection_name=collectionName,
        persist_directory=os.getenv("CHROMA_DIRECTORY")
    )

    # searchResult = chromaService.ChromaSearch(collectionName,summary,scene,chracters,vectorStore,embeddingModel)
    searchResult = chromaService.ChromaSearch(collectionName,searchText,vectorStore,embeddingModel)
    response = {
      "searchResult": searchResult
    }

    return jsonify(response)


@chromaNamespace.route('/delete')
class ChromaDelete(Resource):
  @chromaNamespace.expect(chromaNamespace.model(ChromaDelete["title"], ChromaDelete["explanation"]))
  @chromaNamespace.doc(description="벡터 DB에서 해당 컬렉션 삭제 합니다")
  def delete(self):
    """벡터DB 해당 컬렉션 일부 데이터 삭제 API"""
    collectionName = request.get_json().get("collectionName")

    vectorStore = Chroma(
        collection_name=collectionName,
        persist_directory=os.getenv("CHROMA_DIRECTORY")
    )

    chromaService.ChromaDelete(vectorStore)

    return "컬렉션 삭제 완료"



