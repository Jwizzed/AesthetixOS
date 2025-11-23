import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import uuid
import logging

logger = logging.getLogger(__name__)

class MinIOService:
    def __init__(self, bucket_name=None):
        # Internal client for backend operations (create bucket, etc.)
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION),
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # Public client specifically for generating presigned URLs accessible by the frontend
        self.s3_public_client = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_PUBLIC_ENDPOINT_URL, # Use localhost:9000 here
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION),
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Default to clinic-images if not specified, but allow override for other modules
        self.bucket_name = bucket_name or 'aesthetix-uploads'
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
            except Exception as e:
                logger.error(f"Error creating bucket {self.bucket_name}: {e}")

    def generate_presigned_url(self, file_extension='jpg', content_type=None, folder='uploads'):
        """
        Generates a Presigned URL for the client to upload directly.
        Returns:
            - upload_url: The full URL to PUT the file to.
            - object_key: The key (path) to save in the database.
        """
        object_name = f"{folder}/{uuid.uuid4()}.{file_extension}"
        
        # Default content type if not provided
        if not content_type:
            content_type = f'image/{file_extension}'
        
        try:
            # Use the public client to generate the URL
            # This ensures the Host header signature matches what the browser sends (localhost:9000)
            url = self.s3_public_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name,
                    'ContentType': content_type
                },
                ExpiresIn=3600  # 1 hour
            )
            
            return url, object_name
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None, None

