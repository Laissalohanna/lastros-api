from db.session_manager import DBConnectionHandler
from db.models import ProjectConfig


class ProjectConfigRepository:
    def __init__(self):
        self.db_handler = DBConnectionHandler()
        self.db = self.db_handler.__enter__()

    def __del__(self):
        self.db_handler.__exit__(None, None, None)

    def get_by_project_uid(self, project_uid:str):
        
        return self.db.session.query(ProjectConfig).filter_by(
            ProjectUid=project_uid
        ).first()


    def get_all(self, limit=100):
        return self.db.session.query(ProjectConfig).limit(limit).all()


    def create(self, data: dict):
        obj = ProjectConfig(**data)
        self.db.session.add(obj)
        return obj

    def delete(self, project_uid_id):
        obj = self.db.session.query(ProjectConfig).filter(ProjectConfig.Id == project_uid_id).first()
        if obj:
            self.db.session.delete(obj)
        return obj
