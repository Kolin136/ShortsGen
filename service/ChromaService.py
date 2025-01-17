from flask import current_app,g
from langchain_chroma import Chroma
from repository.VideoCaptioningRepository import VideoCaptioningRepository
from repository.VideoRepository import VideoRepository
from service.GeminiService import GeminiService
from langchain_core.documents import Document

videoCaptioningRepository = VideoCaptioningRepository()
videoRepository = VideoRepository()

class ChromaService:
  def ChromaSave(self,videoIdList,vectorStore,collectionName):
    #백터 DB에 저장할 VideoCaptioning 데이터들 가져오기
    videoCaptionings = videoCaptioningRepository.findByVideoId(videoIdList)
    # 임베딩을 위해 VideoCaptioning 모든 컬럼 내용 텍스트로 합치는 작업, 각 VideoCaptioning 데이터에 해당하는 메타데이터 정리
    videoCaptioningDic = self.prepareVideoCaptioningData(videoCaptionings)

    documents = []
    for idx in range(len(videoCaptionings)):
        documents.append(Document(
            page_content=videoCaptioningDic["contents"][idx],
            metadata=videoCaptioningDic["metadatas"][idx])
        )

    # add_documents는 랭체인에서 제공하는 백터 DB에 임베딩후 저장하는 메소드
    vectorStore.add_documents(documents=documents)

    # videoIdList에 담긴 각 비디오 객체에 collectionName 정보를 넣는다
    videoRepository.updateChromaCollectionNameIds(videoIdList,collectionName)

  def ChromaSearch(self,summary,scene,chracters,vectorStore,embeddingModel):

    searchText = (
      f"[summary] {summary} "
      f"[scene] {scene} "
      f"[characters] {chracters}"
    )

    searchResult = vectorStore.similarity_search_by_vector(embedding=embeddingModel.embed_query(searchText), k=7)

    result = [doc.metadata for doc in searchResult]

    return result

  def ChromaDelete(self,vectorStore):

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
        "timecode": videoCaptioning.timecode,
        "start_time": videoCaptioning.start_time,
        "end_time": videoCaptioning.end_time,
      })

      ids.append(videoCaptioning.id)

    return {"contents": contents, "metadatas": metadatas, "ids": ids}



