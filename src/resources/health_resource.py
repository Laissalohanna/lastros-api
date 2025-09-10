class HealthResource:
    def on_get(self, req, resp):
        resp.media = {"status": "ok"}
