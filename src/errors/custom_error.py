class CustomError(Exception):
    """Base class for custom exceptions."""
    status_code = 500 

    def __init__(self, message: str, translate: str = None):
        super().__init__(message)
        self.message = message
        self.translate = translate or message

    def to_dict(self):
        return {
            "error": self.message,
            "translate": self.translate
        }

class NotFoundProjectUID(CustomError):
    status_code = 404 

    def __init__(self, project_uid: str):
        message = f"The project Uid with key: {project_uid}, was not found."
        translate = f"O projeto com a chave: {project_uid}, não foi encontrado."
        super().__init__(message, translate)


class NotFoundFileName(CustomError):
    status_code = 404 

    def __init__(self, file_name: str, project_uid: str):
        message = f"Could not find file with name: {file_name}, for project: {project_uid}."
        translate = f"Não foi possível encontrar o arquivo com o nome: {file_name}, para o projeto: {project_uid}."
        super().__init__(message, translate)
