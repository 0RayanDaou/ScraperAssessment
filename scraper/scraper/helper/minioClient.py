from minio import Minio
from io import BytesIO

class MinioClient:
    """
        MinIO will be used the object storage location. 
        This class will help connect to it and upload files.

    """

    def __init__(self):
        """
            Connect to MinIO service running in Docker.
            The below details in connection are the same as the one defined in docker-compose.yaml

        """
        self.client = Minio(
            endpoint="minio:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )
        # Landing is the location of file we create in.
        self.bucket_name = "landing"

        # Create bucket if it does not exist
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload(self, content: bytes, filename: str):
        """
            This method uploads files to minio  

        Args:
        ---------------------
            content: raw file bytes
            filename: name to store in bucket

        Returns:
        ---------------------
            Path stored in metadata (bucket/key)
        """
        
        data = BytesIO(content)

        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=filename,
            data=data,
            length=len(content),
            content_type="application/octet-stream"
        )

        # This is what you store in MongoDB
        return f"{self.bucket_name}/{filename}"
