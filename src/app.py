import falcon
from resources import HealthResource, BallastsResource
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

ballasts_resource = BallastsResource()
app.add_route("/ballasts/project/{project_uid}/file/{file_name}", ballasts_resource, suffix="by_file_name_and_project_uid")
