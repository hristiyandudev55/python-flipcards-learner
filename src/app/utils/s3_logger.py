import logging
from datetime import datetime

import boto3

from app.config import AWS_ACCESS_KEY, AWS_BUCKET_NAME, AWS_REGION, AWS_SECRET_KEY


class S3Logger:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )
        self.bucket_name = AWS_BUCKET_NAME
        self.log_folder = "logs"

    def upload_log(self, log_data: str):
        """
        Uploading log in S3 bucket with current datetime.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{self.log_folder}/log_{timestamp}.txt"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=log_filename,
                Body=log_data.encode("utf-8"),
                ContentType="text/plain",
            )
            print(f"✅ Log successfully uploaded to S3: {log_filename}")
        except Exception as e:
            print(f"❌ Error uploading log: {e}")

    def log_action(self, action: str, details: dict):
        """
        Log application actions with details
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_data = {
            "timestamp": timestamp,
            "action": action,
            "details": details
        } # noqa: F841
        
        log_content = f"""
Timestamp: {timestamp}
Action: {action}
Details: {details}
------------------------
"""
        
        log_filename = f"{self.log_folder}/{action}_{timestamp}.txt"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=log_filename,
                Body=log_content.encode("utf-8"),
                ContentType="text/plain",
            )
            print(f"✅ Action logged to S3: {action}")
        except Exception as e:
            print(f"❌ Error logging action: {e}")

s3_logger = S3Logger()
