from minio import Minio
from io import BytesIO
import os

class MinioClient:
    """
        MinIO will be used as the object storage location. 
        This class will help connect to it and upload files.

    """

    def __init__(self, bucketName='landing'):
        """
            Connect to MinIO service running in Docker or locally.
            The below details in connection are the same as the one defined in docker-compose.yaml
            
        """
        minio_host = os.getenv('MINIO_HOST', 'localhost')
        self.client = Minio(endpoint=f"{minio_host}:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)
        # Landing is the location of file we create in.
        self.bucket_name = bucketName
    
        # Create bucket if it does not exist
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload(self, objectPath, raw_content):
        """
            This method uploads files to minio  

        Args:
        ---------------------
            objectPath: path of the file to be uploaded to bucket
            raw_content: raw file bytes

        Returns:
        ---------------------
            Path stored in MinIO (bucket/objectPath)
        """
        # treansform raw binary content into a file like object 
        data = BytesIO(raw_content)

        self.client.put_object(bucket_name=self.bucket_name, object_name=objectPath, data=data, length=len(raw_content), content_type="application/octet-stream")

        # This is what you store in MongoDB as filePath
        return f"{self.bucket_name}/{objectPath}"
    
    def download(self, objectPath):
        """
            This method downloads files from minio  

        Args:
        ---------------------
            objectPath: path of the file to be downloaded from bucket

        Returns:
        ---------------------
            rawContent: raw file bytes
        """
        response = self.client.get_object(bucket_name=self.bucket_name, object_name=objectPath)

        rawContent = response.read()
        response.close()
        response.release_conn()
        return rawContent
