from datetime import datetime
import hashlib
from scraper.helper.minioClient import MinioClient
from scraper.helper.mongoClient import MongoDBClient
import os, io

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
        # Initiate MinIO Client
        # access key and secret key defined in the docker-compose.yaml
        self.lnd_minio_client = MinioClient(bucketName='landing')
        # Initialize Mongo Client to handle MongoDB operations
        # Database name found in class
        self.mongo_client = MongoDBClient()
        # Get both landing and staging collections
        self.lnd_collection = self.mongo_client.getCollection('lnd_documents_metadata')
        self.lnd_bucket = 'landing'


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

        items keys: Id, title, description, date, partition_date, body, sourceURL, documentURL, fileType, filePath, fileHash

        Args:
        ---------------------
            item: the scraped item
            spider: the spider currently open
        Return:
        ---------------------
            item: the scraped item
        """
        raw_content = item['rawContent']
        # Generate a SHA-256 cryptographic hash and returns hexadecimal string
        fileHash = hashlib.sha256(raw_content).hexdigest()
        item['fileHash'] = fileHash
        extension = item['fileType']
        # Object Path directs to the location in MinIO
        objectPath = f"{item['body']}_{item['partition_date']}/{item['Id']}.{extension}"
        # upload file to bucket
        self.lnd_minio_client.upload(objectPath=objectPath, raw_content=raw_content)
        # Construct MinIO filePath
        item['filePath'] = f"{self.lnd_bucket}/{objectPath}"
        # Remove items not needed to be inserted in MongoDB in the returned items (metadata)
        item.pop('rawContent', None)
        item.pop('body', None)

        # Upsert metadata to make sure than when scraping there are no duplicate values in the database
        self.mongo_client.upsertItem(self.lnd_collection.name, {'Id': item['Id']}, item)

        return item
