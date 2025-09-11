from db.session_manager import DBConnectionHandler
from db.models import BaseFiles


class VuonPrdRepository:
    def __init__(self):
        self.db_handler = DBConnectionHandler()
        self.db = self.db_handler.__enter__()

    def __del__(self):
        self.db_handler.__exit__(None, None, None)

    def get_by_project_uid(self, project_uid:str):
        return

    def get_by_file_name(self, file_name, project_uid):
        return self.db.session.query(BaseFiles).filter_by(
            FileName=file_name,
            ProjectUid=project_uid
        ).first()

    def get_all(self, limit=100):
        return self.db.session.query(BaseFiles).limit(limit).all()


    def create(self, data: dict):
        obj = BaseFiles(**data)
        self.db.session.add(obj)
        return obj

    def delete(self, file_id):
        obj = self.db.session.query(BaseFiles).filter(BaseFiles.Id == file_id).first()
        if obj:
            self.db.session.delete(obj)
        return obj
