from flask import jsonify

class CustomException(Exception):
  """Custom exception for service errors."""
  def __init__(self, message, detailMessage, status_code=400):
    super().__init__(message)
    self.message = message
    self.detailMessage = detailMessage
    self.status_code = status_code


def registerErrorHandlers(app):
  """Register common error handlers."""
  @app.errorhandler(CustomException)
  def handle_service_exception(e):
    response = jsonify({
      "message": e.message,
      "detailMessage": e.detailMessage
    })
    response.status_code = e.status_code
    return response
