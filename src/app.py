import falcon
from routes.health import HealthResource
from routes.users import UsersResource
from middlewares.logging import LoggingMiddleware
from middlewares.error_handler import ErrorHandlerMiddleware
from middlewares.auth import AuthMiddleware
from middlewares.cors import CORSMiddleware

# Inicializa API com middlewares
app = falcon.App(
    middleware=[
        LoggingMiddleware(),
        ErrorHandlerMiddleware(),
        AuthMiddleware(),
        CORSMiddleware()
    ]
)

# Rotas
app.add_route("/health", HealthResource())
app.add_route("/users", UsersResource())
