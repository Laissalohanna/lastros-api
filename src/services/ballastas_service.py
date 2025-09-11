
from controllers import BallastsController

class BallastsService:
    def __init__(self):
        self.ballasts_controller = BallastsController()
        
    def get_external_id_by_file_name(self, file_name: str, project_uid: str):
        external_id = self.ballasts_controller.get_external_id_by_file_name(file_name=file_name, project_uid=project_uid)
        return external_id
