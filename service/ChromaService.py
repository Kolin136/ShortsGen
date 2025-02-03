import os
from common.exception.GlobalException import CustomException
from prompt.ChromaSearchPrompt import ChromaSearchPrompt
from repository.VideoCaptioningRepository import VideoCaptioningRepository
from repository.VideoRepository import VideoRepository
from service.GeminiService import GeminiService
from langchain_core.documents import Document
from langchain_chroma import Chroma

videoCaptioningRepository = VideoCaptioningRepository()
videoRepository = VideoRepository()

class ChromaService:
  def chromaSave(self,promptId,embeddingModel,collectionName):
    #백터 DB에 저장할 VideoCaptioning 데이터들 가져오기
    videoCaptioningModelList = videoCaptioningRepository.findByPromptId(promptId)
    if len(videoCaptioningModelList) == 0:
      raise CustomException("해당 프롬프트는 캡셔닝된 데이터가 없습니다.캡셔닝 부터 진행해 주세요",  statusCode=404)

    # 중복 저장 방지를 위해 기존 컬렉션 삭제후 다시 저장
    # 예를들어 프롬프트id 1번,비디오id 1~2번 캡셔닝 데이터 이미 A컬렉션에 저장중인데,이후 프롬프트id 1번 비디오id 3번 캡셔닝 데이터 추가로 A컬렉에
    # 저장할시 프롬프트id 기준으로 캡셔닝 데이터 가져와서 저장하니 비디오id 1~2번 데이터가 중복으로 저장된다. 그러므로 삭제후 다시 저장
    vectorStore = Chroma(
        collection_name=collectionName,
        embedding_function=embeddingModel,
        persist_directory=os.getenv("CHROMA_DIRECTORY")
    )
    vectorStore.delete_collection()

    # 삭제 완료 했으니 저장을 위해 다시 랭체인용 크로마 객체 생성
    vectorStore = Chroma(
        collection_name=collectionName,
        embedding_function=embeddingModel,
        persist_directory=os.getenv("CHROMA_DIRECTORY")
    )

    # 임베딩을 위해 VideoCaptioning 모든 각 컬럼 내용을 텍스트로 합치고, 각 컬럼의 메타데이터 정리
    videoCaptioningDic = self.prepareVideoCaptioningData(videoCaptioningModelList)

    #랭체인으로 벡터 DB 저장하기 위해 Document 객체로 정리
    documents = []
    for idx in range(len(videoCaptioningModelList)):
        documents.append(Document(
            page_content=videoCaptioningDic["contents"][idx],
            metadata=videoCaptioningDic["metadatas"][idx])
        )

    # add_documents는 랭체인에서 제공하는 백터 DB에 임베딩후 저장하는 메소드
    vectorStore.add_documents(documents=documents)

    # promptId에 해당하는 모든 비디오 캡셔닝 객체에 collectionName 정보를 넣는다
    videoCaptioningRepository.updateChromaCollectionNameIds(promptId,collectionName)

  def chromaSearch(self,collectionName,searchText,vectorStore,embeddingModel):
    #클라가 보낸 검색글이 캡셔닝 응답 json 어떤 필드에 해당하는지 프롬프트에 key 종류 넣기 위한 작업
    videoCaptioning = videoCaptioningRepository.findByVideoCollectionNameWithJoin(collectionName)
    excludeKeys = ["타임코드", "시작시간", "종료시간","videoId","videoName"]
    captioningJsonKeyList= [key for key in videoCaptioning.video_analysis_json.keys() if key not in excludeKeys]

    # 클라에서 시나리오 검색 searchText 보낸거로 캡셔닝 응답 json 어떤 필드에 해당하는지 LLM한테 맞춰달라 요청하는 작업
    prompt = ChromaSearchPrompt.prompt(captioningJsonKeyList,searchText)
    chromaSearchText = GeminiService.generalSingletonQuestions(prompt)

    searchResult = vectorStore.similarity_search_by_vector(embedding=embeddingModel.embed_query(chromaSearchText), k=7)

    result = [doc.metadata for doc in searchResult]

    return result

  def chromaDelete(self,vectorStore):

    vectorStore.delete_collection()


  def prepareVideoCaptioningData(self,videoCaptionings):
    contents = []
    metadatas = []
    ids = []

    for idx,videoCaptioning in enumerate(videoCaptionings):
      excludeKeys = ["타임코드", "시작시간", "종료시간","videoId","videoName"]

      combinedText = " ".join([
        f"[{key}] {value}" for key, value in videoCaptioning.video_analysis_json.items() if key not in excludeKeys
      ])

      contents.append(combinedText)

      metadatas.append({
        "video_id": videoCaptioning.video_id,
        "prompt_id": videoCaptioning.prompt_id,
        "timecode": videoCaptioning.timecode,
        "start_time": videoCaptioning.start_time,
        "end_time": videoCaptioning.end_time,
      })

      ids.append(videoCaptioning.id)

    return {"contents": contents, "metadatas": metadatas, "ids": ids}



