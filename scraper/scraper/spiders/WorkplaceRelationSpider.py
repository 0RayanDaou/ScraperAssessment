import scrapy as sp
from pathlib import Path
from scraper.helper.HelperFunction import HelperFunction
from datetime import datetime
from urllib.parse import urlparse, parse_qs

class WorkplaceRelationSpider(sp.Spider):
    """
    This Scraper will be used to scrape the webpage provided in the assessment
    Unique Name: documents
    Way it works:
        Spider → yields Request → Scheduler → Downloader → Response → callback
    """
    name = "documents"

    def __init__(self, start_date, end_date, query, body, partition,*args, **kwargs):
        super().__init__(*args, **kwargs)

        now = datetime.now()
        # Format the datetime object into the specified string format
        logFileName = now.strftime("%Y%m%d%H%M%S") + '_Log.txt'
        # Construct Log File Name and Metadata File Name with Timestamp For different Runs Monitoring
        logFileName = Path('Log') / logFileName
        self.helperClass = HelperFunction('', logFileFullPath = logFileName, loggerLevel='DEBUG')
        self.urls = self.helperClass.constructScrapingList(start_date=start_date, end_date=end_date, query=query, body=body, partition=partition)
    
    def start_requests(self):
        """
            start
        """
        # For each url constructed in helper class constructScrapingList yiel request
        for url in self.urls:
            yield sp.Request(url=url, callback=self.parse, cb_kwargs={'partition_date': self._extract_partition(url)})

    def parse(self, response, partition_date):
        Path('Metadata').mkdir(exist_ok=True)
        metadataFilePath = Path('Metadata') / f'response_{partition_date}.html'
        metadataFilePath.write_bytes(response.body)
        self.logger.info('HTML Saved')
    
    def _extract_partition(self, url):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        # take the "from" date as the partition identifier
        return params["from"][0].replace("/", "-")