from repositories import VuonPrdRepository

class BallastsController:
    def __init__(self):
        self.vuon_prd_repository = VuonPrdRepository

    def get_external_id_by_file_name(self, file_name: str, project_uid: str):
        try:
            file_name = self.vuon_prd_repository.get_by_file_name(file_name=file_name
                                                                  , project_uid=project_uid
                                                                  )
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar no SFTP: {e}")

    def upload_file(self, local_path: str, remote_path: str):
        try:
            self.sftp.put(local_path, remote_path)
            print(f"Arquivo {local_path} enviado para {remote_path}.")
        except Exception as e:
            raise RuntimeError(f"Erro ao enviar arquivo: {e}")

    def delete_file(self, remote_path: str):
        try:
            self.sftp.remove(remote_path)
            print(f"Arquivo {remote_path} removido com sucesso.")
        except Exception as e:
            raise RuntimeError(f"Erro ao remover arquivo: {e}")

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        print("Conexão encerrada.")