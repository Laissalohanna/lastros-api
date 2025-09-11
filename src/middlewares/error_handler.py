import traceback
import falcon
from errors import CustomError

class ErrorHandlerMiddleware:
    def process_response(self, req, resp, resource, req_succeeded):
        if not req_succeeded:
            exc = getattr(req.context, "exception", None)
            if isinstance(exc, CustomError):
                resp.status = falcon.HTTP_500 
                if hasattr(exc, "status_code"):
                    resp.status = str(exc.status_code)
                resp.media = exc.to_dict()
            else:
                resp.status = falcon.HTTP_500
                resp.media = {"error": "Internal Server Error"}
                print("Error:", traceback.format_exc())
