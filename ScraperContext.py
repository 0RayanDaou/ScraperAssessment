from HelperFunction import HelperFunction
from Logger import Logger
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
        # Construct Log File Name with Timestamp For different Runs Monitoring
        logFileName = '_'.join(timestamp_str,'Log.txt')
        # Construct Log Folder as Current Script Location in addition to Logs Folder
        logFilePath = '\\'.join(script_dir, 'Logs')
        # Ensure Log Folder is created
        os.makedirs(logFilePath, exist_ok=True)

        # Construct Full Log Path
        self.logFileFullPath = '\\'.join(logFilePath, logFileName)

        # Initialize Helper Class With Logger Class
        self.hf = HelperFunction('', self.logFileFullPath)


        pass