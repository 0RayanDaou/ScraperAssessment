from scraper.helper.minioClient import MinioClient
from scraper.helper.mongoClient import MongoDBClient
from scraper.helper.HelperFunction import HelperFunction
from scraper.exception.Exception import *
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import hashlib
import os


class Transform:
    """
        This Class will be responsible to traverse and return items based on date range provided. 
        Gets the related files from the database and iterates to check if pdf/doc/docs or html files to apply their respective logic.
        If of type docx/doc/pdf then no change/transofmations else if html then apply transformation to clean the html tags and relative inforation only.
        Rename files to their identifier and store the files in a new storage bucket.
        Store the metadata in a new collection with updated new file path and file hash. 

    """
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        now = datetime.now()
        # Format the datetime object into the specified string format
        logFileName = 'Transforming_' + now.strftime('%Y%m%d%H%M%S') + '_Log.txt'
        # Construct Log File Name with Timestamp For different Runs Monitoring
        logFileName = Path('Log') / logFileName
        # Initialize helper class that will help construct urls based on inputs provided
        self.helperClass = HelperFunction( logFileFullPath = logFileName, loggerLevel='DEBUG')
        self.helperClass.logAction('info', 'Transformation Initiation', 'Done.')
        #Initiate MinIO and MongoDB clients
        self.lndMinioClient = MinioClient(bucketName='landing')
        self.stgMinioClient = MinioClient(bucketName='staging')
        self.mongoClient = MongoDBClient()


    def apply(self):
        """
            Main method to run the transformation process.
            Takes data from landing collection, applies transformations based on file type,
            uploads to staging bucket, and updates metadata in staging collection.
        """
        self.helperClass.logAction('info', 'Transformation Started', 'fetching metadata from landing collection.')
        # Get landing collection
        lndItems = self.mongoClient.finditems('lnd_documents_metadata', self.start_date, self.end_date)
        
        self.helperClass.logAction('info', 'Metadata Fetched', f'Number of items fetched: {len(lndItems)}. Beginning transformation process.')

        stgFolder = f'from_{self.start_date}_to_{self.end_date}'

        for item in lndItems:
            try:
                self.processRecord(item, stgFolder)
            except Exception as e:
                self.helperClass.logAction('error', 'Error in Transformation', f'Error processing item with ID {item["Id"]}: {str(e)}')
        
    def processRecord(self, item, stgFolder):
        """
            Process each record based on file type and apply transformations if needed.
            Upload transformed or original file to staging bucket and update metadata in staging collection.

        Args:
        ---------------------
            item: The metadata item retrieved from landing collection.
            stgFolder: The folder in staging bucket to store the files.

        Returns:
        ---------------------
            None
        """
        lndFilePath = item['filePath']
        lndObjectPath = lndFilePath.replace('landing/', '')
        Id = item['Id']
        extension = lndObjectPath.split('.')[-1].lower()
        rawContent = self.lndMinioClient.download(objectPath=lndObjectPath)

        if extension in ['html', 'htm']:
            # Apply HTML transformation
            rawContent = self.cleanHTML(rawContent)
            self.helperClass.logAction('info', 'HTML Transformation', f'Applied HTML cleaning for item ID {Id}.')
        else:
            self.helperClass.logAction('info', 'No Transformation Needed', f'No transformation applied for item ID {Id} with file type {extension}.')
        
        # Generate new file hash
        fileHash = hashlib.sha256(rawContent).hexdigest()

        stgObjectPath = f"{stgFolder}/{Id}.{extension}"

        # Upload to staging bucket
        stgFilePath = self.stgMinioClient.upload(stgObjectPath, rawContent)
        self.helperClass.logAction('info', 'File Uploaded to Staging', f'Uploaded item ID {Id} to staging bucket at {stgFilePath}.')
        # Update metadata
        item['filePath'] = stgFilePath
        item['fileHash'] = fileHash
        item['processedDate'] = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')

        # Upsert into staging collection
        self.mongoClient.upsertItem('stg_documents_metadata', {'Id': Id}, item)
        self.helperClass.logAction('info', 'Metadata Upserted to Staging', f'Upserted metadata for item ID {Id} into staging collection.')


    def cleanHTML(self, rawContent):
        """
            Cleans HTML content by removing tags and extracting text.

        Args:
        ---------------------
            rawContent: Raw HTML content in bytes.

        Returns:
        ---------------------
            cleanedContent: Cleaned text content in bytes.
        """
        soup = BeautifulSoup(rawContent, 'lxml')
        main = soup.find('main') or soup.find('div', {'class': 'main-content'}) or soup.body
        text = main.get_text(' ', strip=True) if main else soup.get_text(' ', strip=True)

        return text.encode('utf-8')
    
    def run(self):
        """
            Runs the transformation process.
        """
        self.helperClass.logAction('info', 'Transformation Run', f'Starting transformation from {self.start_date} to {self.end_date}.'
        )
        self.apply(None)

if __name__ == "__main__":
    start_date = os.getenv("TRANSFORM_START_DATE")
    end_date = os.getenv("TRANSFORM_END_DATE")

    if not start_date or not end_date:
        raise ValueError("TRANSFORM_START_DATE and TRANSFORM_END_DATE must be set")

    transform = Transform(start_date=start_date, end_date=end_date)
    transform.run()