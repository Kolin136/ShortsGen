from flask_restx import Namespace, Resource
from flask import request,url_for, send_file, Response, stream_with_context,render_template,Flask,make_response

# 네임스페이스
templateNamespace = Namespace('5.TemplateRender',description='TemplateRender api 목록')


@templateNamespace.route('/index')
class index(Resource):
  def get(self):
    response = make_response(render_template("index.html"))
    response.headers["Content-Type"] = "text/html"
    return response


@templateNamespace.route('/captioning')
class captioning(Resource):
  def get(self):
    response = make_response(render_template("captioning.html"))
    response.headers["Content-Type"] = "text/html"
    return response


@templateNamespace.route('/shortsinven')
class shortsinven(Resource):
  def get(self):
    response = make_response(render_template("shortsinven.html"))
    response.headers["Content-Type"] = "text/html"
    return response
