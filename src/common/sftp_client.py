import paramiko
from contextlib import contextmanager


class SFTPClient:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.transport = None
        self.sftp = None

    def connect(self):
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            print("Conectado com sucesso ao SFTP.")
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