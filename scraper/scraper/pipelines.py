from pymongo import MongoClient
from datetime import datetime
import hashlib
from minio import Minio
from minio.error import S3Error

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraperPipeline:
    """
        The pipelines class exist to enable and coordinate a pipelines.
        Pipelines:
            Spider opening
            Retrieval of response and parsing
            Computing required data (ex: hash)
            Uploading to MinIO
            inserting metadata to MongoDB
    """
    def open_spider(self, spider):
        """
        This method is called when the spider is opened. (From Docs)
        Open connection to mongo db in order to writer metadata, open conenction to MinIO to upload files
        
        Args:
        ---------------------
            spider: the spider opened to extract data
        """

        self.mongo_client = MongoClient('mongodb://mongo:27017')
        # Database name, will be able to create or reuse database
        self.db = self.mongo_client['WorkplaceRelation_metadata']
        # Decision collection in mongo db to store metadata as requested and defined in items.py
        self.collection = self.db['documents_metadata']
        # Initiate MinIO Client
        # access key and secret key defined in the docker-compose.yaml
        self.minio_client = Minio('minio:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)
        self.bucket = 'landing'

        # Make sure to create bucket if not exists
        if not self.minio_client.bucket_exists(self.bucket):
            self.minio_client.make_bucket(self.bucket)


    def close_spider(self, spider):
        """
        Closes the connection created by the spider when it finishes. (From Docs)
        
        Args:
        ---------------------
            spider: the spider opened to extract data
        """
        self.mongo_client.close()

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component. (From Docs)
            Must either: return an item object, return a Deferred or raise a DropItem exception.
            Dropped items are no longer processed by further pipeline components.
        In this case, the item returned will have its content read, the content hashed, uploaded to MinIO for storage, and then inserted to MongoDB
        with the requested data as per assessment. 

        items keys: Id, title, description, date, fileLink, partition_date, body, sourceURL, documentURL, fileType, filePath, fileHash

        Args:
        ---------------------
            item: the scraped item
            spider: the spider currently open
        Return:
        ---------------------
            item: the scraped item
        """
        raw_content = item['rawContent']
        fileHash = hashlib.sha256(raw_content).hexdigest
        item['fileHash'] = fileHash
        extension = item['fileType']
        objectPath = f'{item['partition_date']}/{item['id']}.{extension}'

        self.minio_client.put_object(bucket_name=self.bucket, object_name=objectPath, data=raw_content, length=len(raw_content), content_type='application/octet-stream')

        item['filePath'] = f'{self.bucket}/{objectPath}'
        self.collection.insert_one(dict(item))

        return item
