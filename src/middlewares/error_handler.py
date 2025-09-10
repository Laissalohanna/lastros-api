import traceback
import falcon

class ErrorHandlerMiddleware:
    def process_response(self, req, resp, resource, req_succeeded):
        if not req_succeeded:
            resp.status = falcon.HTTP_500
            resp.media = {"error": "Internal Server Error"}
            print("Error:", traceback.format_exc())
