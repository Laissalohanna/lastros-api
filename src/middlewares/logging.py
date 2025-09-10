import time

class LoggingMiddleware:
    def process_request(self, req, resp):
        req.context.start_time = time.time()

    def process_response(self, req, resp, resource, req_succeeded):
        duration = time.time() - req.context.start_time
        print(f"{req.method} {req.url} - {duration:.4f}s")
