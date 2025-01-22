class ChromaSearchPrompt:
  @staticmethod
  def prompt(captioningJsonKeyList,searchText):
    return f"""
    다음 텍스트를 분석해서 JSON 키에 맞는 형식으로 출력해 주세요.

    텍스트: {searchText}

    JSON 키: {captioningJsonKeyList}

    출력 형식 예시:
    "[{captioningJsonKeyList[0]}] <{captioningJsonKeyList[0]}에 대한 텍스트 내용> [{captioningJsonKeyList[1]}] <{captioningJsonKeyList[1]}에 대한 텍스트 내용>...

    Json 형식으로 출력 하는게 아닌 반드시 위에 형식에 맞춰서 출력해 주세요.
    """