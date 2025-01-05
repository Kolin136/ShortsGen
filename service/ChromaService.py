from flask import current_app,g
from langchain_chroma import Chroma
from repository.VideoClipRepository import VideoClipRepository
from service.GeminiService import GeminiService
from langchain_core.documents import Document

videoClipRepository = VideoClipRepository()

class ChromaService:
  def ChromaSave(self,videoIdList,vectorStore):
    #백터 DB에 저장할 videoClip 데이터들 가져오기
    videoClips = videoClipRepository.findByVideoId(videoIdList)
    # 임베딩을 위해 videoClips 모든 컬럼 내용 텍스트로 합치는 작업, 각 videoClips 데이터에 해당하는 메타데이터 정리
    videoClipDic = self.prepareVideoClipData(videoClips)

    documents = []
    for idx in range(len(videoClips)):
        documents.append(Document(
            page_content=videoClipDic["contents"][idx],
            metadata=videoClipDic["metadatas"][idx])
        )

    vectorStore.add_documents(documents=documents)

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


  def prepareVideoClipData(self,videoClips):
    contents = []
    metadatas = []
    ids = []

    for idx,videoClip in enumerate(videoClips):
      combinedText = (
        f"[summary] {videoClip.summary} "
        f"[action] {videoClip.action} "
        f"[scene_description] {videoClip.scene_description} "
        f"[emotion] {videoClip.emotion} "
        f"[scene] {videoClip.scene} "
        f"[characters] {videoClip.characters}"
      )
      contents.append(combinedText)

      metadatas.append({
        "video_id": videoClip.video_id,
        "timecode": videoClip.timecode,
        "start_time": videoClip.start_time,
        "end_time": videoClip.end_time,
      })

      ids.append(videoClip.id)

    return {"contents": contents, "metadatas": metadatas, "ids": ids}



