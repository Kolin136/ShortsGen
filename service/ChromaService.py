from flask import current_app,g

from repository.VideoClipRepository import VideoClipRepository
from service.GeminiService import GeminiService


videoClipRepository = VideoClipRepository()

class ChromaService:
  def ChromaSave(self,videoIdList,collectionName):
    #백터 DB에 저장할 videoClip 데이터들 가져오기
    videoClips = videoClipRepository.findByVideoId(videoIdList)

    collection = g.chromaClient.get_or_create_collection(name=collectionName) # 해당 컬렉션이 있으면 가져오고 없으면 생성하는 메소드

    videoClipDic = self.prepareVideoClipData(videoClips)

    embeddingResult = GeminiService.geminiEmbedding(videoClipDic["contents"])

    collection.add(
        embeddings = embeddingResult,
        metadatas=videoClipDic["metadatas"],
        # ids=videoClipDic["ids"]
    )


  def ChromaSearch(self,collectionName,summary,scene,chracters):
    collection = g.chromaClient.get_or_create_collection(name=collectionName)
    searchText = (
      f"[summary] {summary} "
      f"[scene] {scene} "
      f"[characters] {chracters}"
    )

    embeddingResult = GeminiService.geminiEmbedding([searchText])

    searchResult = collection.query(
        query_embeddings=embeddingResult[0],
        include=["metadatas"],
        n_results=7

    )

    return searchResult["metadatas"][0]

    # all_data = collection.get(ids=["1"] ,include=['embeddings', 'documents', 'metadatas'])
    # https://stackoverflow.com/questions/76482987/chroma-database-embeddings-none-when-using-get
    # all_data = collection.get(ids=["1"])
    # print(all_data)
    # collection.delete(
    #     ids=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    # )

  def ChromaDelete(self,collectionName):
    collection = g.chromaClient.get_or_create_collection(name=collectionName)
    collection.delete()



  def prepareVideoClipData(self,videoClips):
    contents = []
    metadatas = []
    ids = []

    for idx,videoClip in enumerate(videoClips,start = 1):
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

      ids.append(str(videoClip.id))

    return {"contents": contents, "metadatas": metadatas, "ids": ids}



