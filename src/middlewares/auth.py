import falcon

class AuthMiddleware:
    def process_request(self, req, resp):
        if req.path.startswith("/users"):
            token = req.get_header("Authorization")
            if not token or token != "Bearer mysecrettoken":
                raise falcon.HTTPUnauthorized(
                    title="Auth Error",
                    description="Missing or invalid token",
                )
