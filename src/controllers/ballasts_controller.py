from repositories import VuonPrdRepository, ProjectConfigRepository
from errors import NotFoundProjectUID, NotFoundFileName


class BallastsController:
    def __init__(self):
        self.vuon_prd_repository = VuonPrdRepository()
        self.project_config_repository = ProjectConfigRepository()

    def get_external_id_by_file_name(self, file_name: str, project_uid: str):
        try:
            project_config = self.project_config_repository.get_by_project_uid(project_uid=project_uid)
            if project_config is None:
                raise NotFoundProjectUID(project_uid=project_uid)

            file_entity = self.vuon_prd_repository.get_by_file_name(
                file_name=file_name, project_uid=project_uid
            )
            if file_entity is None:
                raise NotFoundFileName(file_name=file_name, project_uid=project_uid)

            return {
                "external_id": file_entity.ExternalId,
                "project_uid": project_uid,
                "file_name": file_name
            }

        except (NotFoundProjectUID, NotFoundFileName):
            raise
        except Exception as e:
            raise ConnectionError(f"Erro ao consultar repositórios: {e}")
