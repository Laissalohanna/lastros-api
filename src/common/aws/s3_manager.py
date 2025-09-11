import boto3
import os
from typing import List, Optional

class S3Manager:
    def __init__(self, aws_access_key: str, aws_secret_key: str, region: str = "us-east-1"):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

    def list_files(self, bucket: str, prefix: str = "", extension: Optional[str] = None) -> List[str]:
        paginator = self.s3.get_paginator("list_objects_v2")
        files = []
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if extension is None or key.endswith(extension):
                    files.append(key)
        return files

    def upload_file(self, file_path: str, bucket: str, key: Optional[str] = None) -> str:
        if key is None:
            key = os.path.basename(file_path)
        self.s3.upload_file(file_path, bucket, key)
        return f"s3://{bucket}/{key}"

    def download_file(self, bucket: str, key: str, dest_path: str) -> str:
        self.s3.download_file(bucket, key, dest_path)
        return dest_path

    def download_files(self, bucket: str, prefix: str = "", dest_dir: str = ".", extension: Optional[str] = None) -> List[str]:
        os.makedirs(dest_dir, exist_ok=True)
        files = self.list_files(bucket, prefix, extension)
        downloaded_files = []
        for key in files:
            local_path = os.path.join(dest_dir, os.path.basename(key))
            self.download_file(bucket, key, local_path)
            downloaded_files.append(local_path)
        return downloaded_files

    def delete_file(self, bucket: str, key: str):
        self.s3.delete_object(Bucket=bucket, Key=key)

    def delete_files(self, bucket: str, prefix: str = "", extension: Optional[str] = None) -> List[str]:
        files = self.list_files(bucket, prefix, extension)
        for key in files:
            self.delete_file(bucket, key)
        return files
