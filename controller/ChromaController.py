import os
from chromadb.errors import InvalidCollectionException
from flask import Blueprint, jsonify, request, current_app, g
from flask_restx import Namespace, Resource
from service.ChromaService import ChromaService
from swagger.model.ChromaSwaggerModel import *
from langchain_chroma import Chroma
from common.exception.GlobalException import CustomException

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
    chromaService.chromaSave(videoIdList, vectorStore, collectionName)

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

    # 랭체인을 이용한 크로마 객체 초기화
    try:
      vectorStore = createLangChainVectorStore(collectionName)
    except InvalidCollectionException as e:
      raise CustomException(f"{collectionName} 는 존재하지 않는 컬렉션입니다", str(e), 404)

    embeddingModel = current_app.config['embeddings']
    searchResult = chromaService.chromaSearch(collectionName, searchText, vectorStore, embeddingModel)

    response = {
      "searchResult": searchResult
    }

    return response


@chromaNamespace.route('/delete')
class ChromaDelete(Resource):
  @chromaNamespace.expect(chromaNamespace.model(ChromaDelete["title"], ChromaDelete["explanation"]))
  @chromaNamespace.doc(description="벡터 DB에서 해당 컬렉션 삭제 합니다")
  def delete(self):
    """벡터DB 해당 컬렉션 일부 데이터 삭제 API"""
    collectionName = request.get_json().get("collectionName")

    try:
      vectorStore = createLangChainVectorStore(collectionName)
    except InvalidCollectionException as e:
      raise CustomException(f"{collectionName} 는 존재하지 않는 컬렉션입니다", str(e), 404)

    chromaService.chromaDelete(vectorStore)

    return "컬렉션 삭제 완료"

@chromaNamespace.route('/collections')
class ChromaCollections(Resource):
  @chromaNamespace.doc(description="벡터DB에 존재하는 모든 컬렉션 이름을 조회 합니다.")
  def get(self):
    """벡터DB 컬렉션 종류 모두 조회"""
    embeddingModel = current_app.config['embeddings']
    vectorStore = Chroma(
        collection_name="dummy_collection",
        embedding_function=embeddingModel,
        persist_directory=os.getenv("CHROMA_DIRECTORY"),
    )
    chromaClient = vectorStore._client   # ._client 는 내부 크로마 클라이언트 가져오기
    collectionList =[collection.name for collection in chromaClient.list_collections()]  # 현재 크로마에 존재하는 컬렉션 종류 다 가져오기
    response = {
      "collections": collectionList
    }
    return response

@chromaNamespace.route('/collection/<collection_name>')
class ChromaCollectionDetail(Resource):
  @chromaNamespace.doc(description="벡터DB에 해당 컬렉션의 데이터 모두 조회 합니다.")
  def get(self,collection_name):
    """벡터DB 해당 컬렉션 데이터 조회"""
    # 패스 파라미터값 가져오기
    collectionName = collection_name
    try:
      vectorStore = createLangChainVectorStore(collectionName)
    except InvalidCollectionException as e:
      raise CustomException(f"{collectionName} 는 존재하지 않는 컬렉션입니다", str(e), 404)

    chromaClient = vectorStore._client
    collectionData = chromaClient.get_collection(name=collectionName).get() # 해당 컬렉션안에 모든 데이터 다 가져오기

    response = {
      "collections": collectionData
    }
    return response

def createLangChainVectorStore(collectionName):
  # 랭체인을 이용한 임베딩+벡터DB 생성
  embeddingModel = current_app.config['embeddings']
  return Chroma(
      collection_name=collectionName,
      embedding_function=embeddingModel,
      persist_directory=os.getenv("CHROMA_DIRECTORY"),
      create_collection_if_not_exists=False  # 존재하지 않으면 예외 발생
  )