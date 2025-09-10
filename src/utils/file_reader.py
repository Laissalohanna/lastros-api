import pandas as pd

class FileReader:
    @staticmethod
    def read_file(file_path: str):
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Formato de arquivo não suportado. Use CSV ou XLSX.")
