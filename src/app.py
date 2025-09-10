import falcon
from resources import HealthResource
from middlewares import (LoggingMiddleware, ErrorHandlerMiddleware, AuthMiddleware, CORSMiddleware)

app = falcon.App(
    middleware=[
        LoggingMiddleware(),
        ErrorHandlerMiddleware(),
        AuthMiddleware(),
        CORSMiddleware()
    ]
)

app.add_route("/health", HealthResource())
