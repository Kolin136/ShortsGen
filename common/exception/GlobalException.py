from flask import jsonify

class CustomException(Exception):
  """Custom exception for service errors."""
  def __init__(self, message, detailMessage=None, statusCode=400):
    super().__init__(message)
    self.message = message
    self.detailMessage = detailMessage
    self.statusCode = statusCode


def registerErrorHandlers(app):
  """Register common error handlers."""
  @app.errorhandler(CustomException)
  def handle_service_exception(e):
    response = jsonify({
      "message": e.message,
      "detailMessage": e.detailMessage
    })
    response.status_code = e.statusCode
    return response
