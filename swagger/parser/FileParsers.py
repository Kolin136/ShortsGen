from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

# VipdeoSplit Api
videoSplitParser = reqparse.RequestParser()
videoSplitParser.add_argument('video', location='files', type=FileStorage, required=True, help='비디오 파일을 업로드해야 합니다')