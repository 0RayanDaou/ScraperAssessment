from scraper.scraper.helper.HelperFunction import HelperFunction
from scraper.scraper.logger.Logger import Logger
from pathlib import Path
from datetime import datetime
import os


class ScraperContext():
    def __init__(self):
        # Get Current work directory of python script
        script_dir = Path(__file__).resolve().parent
        now = datetime.now()
        # Format the datetime object into the specified string format
        timestamp_str = now.strftime("%Y%m%d%H%M%S")
        # Construct Log File Name and Metadata File Name with Timestamp For different Runs Monitoring
        logFileName = '_'.join(timestamp_str,'Log.txt')
        metadatFileName = '_'.join(timestamp_str,'Metadata.txt')
        # Construct Log Folder as Current Script Location in addition to Logs Folder
        logFilePath = '\\'.join(script_dir, 'Logs')
        # Construct Metadata Folder as Current Script Location in addition to Metadata Folder
        metadataFilePath = '\\'.join(script_dir, 'Metadata')
        # Ensure Needed Folders are Created
        os.makedirs(logFilePath, exist_ok=True)
        os.makedirs(metadataFilePath, exist_ok=True)
        # Construct Full Log Path
        self.logFileFullPath = '\\'.join(logFilePath, logFileName)
        self.metadataFileFullPath = '\\'.join(metadataFilePath, metadatFileName)
        # Initialize Helper Class With Logger Class
        self.hf = HelperFunction('', self.logFileFullPath)



        pass