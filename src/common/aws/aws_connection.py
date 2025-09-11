import boto3

class AWSConnection:
    def __init__(self, aws_access_key: str, aws_secret_key: str, region: str = "us-east-1"):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region = region

    def get_s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region
        )