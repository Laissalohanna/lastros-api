from services import BallastsService

class BallastsResource:
    def __init__(self):
        self.ballasts_service = BallastsService()

    def on_get(self, req, resp, project_uid, file_name):
        external_id = self.ballasts_service.get_external_id_by_file_name(
            file_name=file_name,
            project_uid=project_uid
        )
        resp.media = {"external_id": external_id}
