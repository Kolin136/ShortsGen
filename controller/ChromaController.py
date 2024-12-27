from flask import Blueprint,jsonify ,request

from service.ChromaService import ChromaService


# Blueprint 정의
chromaController = Blueprint('chromaController', __name__)

chromaService = ChromaService()

@chromaController.route("/chroma/save", methods=["POST"])
def ChromaSave():
  videoIdList = request.get_json().get("videoIdList",[])
  collectionName = request.get_json().get("collectionName")

  chromaService.ChromaSave(videoIdList,collectionName)

  return jsonify("크로마 DB 저장 완료")


@chromaController.route("/chroma/search", methods=["POST"])
def ChromaSearch():
  # searchText = request.get_json().get("searchText")
  collectionName = request.form.get("collectionName")
  summary = request.form.get("summary")
  scene = request.form.get("scene")
  chracters = request.form.get("chracters")

  searchResult = chromaService.ChromaSearch(collectionName,summary,scene,chracters)

  response = {
    "searchResult" : searchResult
  }

  return jsonify(response)

@chromaController.route("/chroma/delete", methods=["DELETE"])
def ChromaDelete():
  collectionName = request.get_json().get("collectionName")
  deleteIds = request.get_json().get('ids')

  chromaService.ChromaDelete(collectionName,deleteIds)


  return "삭제 완료"

