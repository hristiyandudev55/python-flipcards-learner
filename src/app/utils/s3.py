from datetime import datetime
import io
import os
import uuid

import boto3
from fastapi import HTTPException, UploadFile
from PIL import Image
from app.config import AWS_ACCESS_KEY, AWS_BUCKET_NAME, AWS_REGION, AWS_SECRET_KEY


class S3Service:
    MAX_SIZE = (300, 300)
    ALLOWED_FORMATS = {".jpg", ".jpeg", ".png", ".svg"}
    JPEG_QUALITY = 90
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

    def __init__(self):
        self.bucket_name = AWS_BUCKET_NAME
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )

    def validate_image(self, file: UploadFile) -> None:
        """
        Validates the uploaded image file.

        This method checks if the file format is allowed and if the file size
        is within the maximum limit.

        Args:
            file (UploadFile): The uploaded image file to be validated.

        Raises:
            HTTPException: If the file format is not allowed or if the file size
            exceeds the maximum limit.
        """
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in self.ALLOWED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. "
                f"Allowed formats: {', '.join(self.ALLOWED_FORMATS)}",
            )

        # Check file size
        file.file.seek(0, 2)  # end of the file
        size = file.file.tell()  # current position
        file.file.seek(0)  # return to the beginning

        if size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. "
                f"Maximum size is {self.MAX_FILE_SIZE / 1024 / 1024}MB",
            )

    def process_image(self, image_data: bytes) -> bytes:
        """
        Processes the uploaded image data.

        This method opens the image, converts it to RGB if needed,
        resizes it if it exceeds the maximum size, and optimizes it before
        converting it back to bytes.

        Args:
            image_data (bytes): The raw image data to be processed.

        Returns:
            bytes: The processed image data in bytes.

        Raises:
            HTTPException: If there is an error processing the image.
        """
        try:
            image = Image.open(io.BytesIO(image_data))

            # Convert to RGB if needed
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Resize if needed
            if image.size[0] > self.MAX_SIZE[0] or image.size[1] > self.MAX_SIZE[1]:
                image.thumbnail(self.MAX_SIZE, Image.Resampling.LANCZOS)

            # Optimize and convert to bytes
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=self.JPEG_QUALITY, optimize=True)
            return output.getvalue()

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error processing image: {str(e)}"
            )

    def upload_file(self, file: UploadFile, folder: str) -> str:
        """
        Uploads a file to an S3 bucket.

        This method generates a unique filename, reads the file content,
        uploads it to the specified S3 bucket,
        and returns the URL of the uploaded file.

        Args:
            file (UploadFile): The file to be uploaded.
            folder (str): The folder in the S3 bucket where the file will be stored.

        Returns:
            str: The URL of the uploaded file.

        Raises:
            HTTPException: If there is an error uploading the file.
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            extension = os.path.splitext(file.filename)[1]
            new_filename = f"{folder}/{timestamp}_{unique_id}{extension}"

            # Read file content
            contents = file.file.read()

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=new_filename,
                Body=contents,
                ContentType=file.content_type,
            )

            # Generate URL
            return f"https://{self.bucket_name}.s3.amazonaws.com/{new_filename}"

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error uploading file: {str(e)}"
            )
        finally:
            file.file.close()

    def delete_file(self, file_url: str) -> bool:
        """
        Deletes a file from an S3 bucket.

        This method extracts the key from the given file URL and deletes
        the corresponding file from the S3 bucket.

        Args:
            file_url (str): The URL of the file to be deleted.

        Returns:
            bool: True if the file was successfully deleted or if the file
            URL is empty, False otherwise.

        Raises:
            Exception: If there is an error deleting the file.
        """
        try:
            if not file_url:
                return True

            # Extract key from URL
            key = file_url.split(".com/")[1]

            # Delete from S3
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    # WON'T USE IT NOW AS THE APP DOESNT HAVE PRIVATE ASSETS
    # def generate_presigned_url(self, key: str) -> str:
    #     """Generate a presigned URL for accessing an S3 object."""
    #     try:
    #         url = self.s3_client.generate_presigned_url(
    #             'get_object',
    #             Params={
    #                 'Bucket': self.bucket_name,
    #                 'Key': key
    #             },
    #             ExpiresIn=3600
    #         )
    #         return url
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=500,
    #             detail=f"Error generating presigned URL: {str(e)}"
    #         )


s3_service = S3Service()
