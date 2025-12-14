import scrapy as sp
from pathlib import Path
from scraper.helper.HelperFunction import HelperFunction
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin
from items import ScraperItem

class WorkplaceRelationSpider(sp.Spider):
    """
    This Scraper will be used to scrape the webpage provided in the assessment
    Unique Name: documents
    Way it works:
        Spider → yields Request → Scheduler → Downloader → Response → callback
    """
    name = "documents"

    def __init__(self, start_date, end_date, query, body, partition,*args, **kwargs):
        """
            Overriding the initialization of Spider to include additional parameters needed to construct the urls
            in the helper class.
            Args:
            ---------------------
                start_date: Start date to get docs, format dd/MM/YYYY Ex: 7/10/2025 or 13/10/2025
                end_date: End date to get docs, format dd/MM/YYYY Ex: 7/10/2025 or 13/10/2025
                query: Query used to search for documents
                body: Selections available in workplacerelations, provided as keywords mapped to ids
                    - Employment Appeals Tribunal: 2
                    - Equality Tribunal: 1
                    - Labour Count: 3
                    - Workplace Relations Commission: 15376
                    Multiple Keywords can be provided at a time separated by a comma
                partition: Select partitioning of dates in days, Ex: 1 for 1 day, 7 for a week, 30 for a month
            Returns:
            ---------------------
                None
        """
        super().__init__(*args, **kwargs)

        now = datetime.now()
        # Format the datetime object into the specified string format
        logFileName = now.strftime("%Y%m%d%H%M%S") + '_Log.txt'
        # Construct Log File Name and Metadata File Name with Timestamp For different Runs Monitoring
        logFileName = Path('Log') / logFileName
        # Initialize helper class that will help construct urls based on inputs provided
        self.helperClass = HelperFunction('', logFileFullPath = logFileName, loggerLevel='DEBUG')
        # hold urls to be called by scraper
        self.urls = self.helperClass.constructScrapingList(start_date=start_date, end_date=end_date, query=query, body=body, partition=partition)
        self.helperClass.logAction('info', 'Spider Initiation', 'Done.')
    
    def start_requests(self):
        """
            Starts the process of yielding requests. 
            Args:
            ---------------------
                None

            Returns:
            ---------------------
                None
        """
        # For each url constructed in helper class constructScrapingList yiel request
        for url in self.urls:
            yield sp.Request(url=url, callback=self.parse, cb_kwargs={'partition_date': self._extract_partition(url)})

    def parse(self, response, partition_date):
        """
            Parses the response retrievd from each url. 
            Fields in ScraperItems: Id, title, description, date, fileLink, partition_date, sourceURL, documentURL, fileType, filePath, fileHash

            Args:
            ---------------------
                response: Url request response
                parition_date: The date retrieved from the from section of the url
                
            Returns:
            ---------------------
                None
        """
        for row in response.css("div.search-result"):
            item = ScraperItem()

            item['Id'] = row.css('.decision-number::text').get()
            item['title'] = row.css('h3 a::text').get()
            item['description'] = row.css('.description::text').get()
            item['date'] = row.css('.decision-date::text').get()
            item['fileLink'] = urljoin(response.url, row.css('h3 a::attr(href)').get()) 
            item["partition_date"] = partition_date
            item["sourceURL"] = response.url
            documentURL = str(urljoin(response.url, row.css('h3 a::attr(href)').get()))
            item['documentURL'] = urljoin(response.url, row.css('h3 a::attr(href)').get()) 

            # gto be populated at a latter level
            item["fileType"] = None
            item["filePath"] = None
            item["fileHash"] = None

            # Decision step to perform requirements as provided in assesment
            # If pdf, doc, docx then call parse_binary
            if documentURL.endswith(('.pdf', '.doc', '.docx')):
                yield response.follow(
                    documentURL,
                    callback=self.parse_binary,
                    meta={'item': item}
                )
            # else parse_html
            else:
                yield response.follow(
                    documentURL,
                    callback=self.parse_html,
                    meta={'item': item}
                )

    def _extract_partition(self, url):
        """
            Extracts the from date from the url.

            Args:
            ---------------------
                url: the url used to extratc the date from
            
            Returns:
            ---------------------
                date: date string with format dd-MM-YYYY Ex: 04-11-2025

        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        # take the "from" date as the partition identifier
        return params["from"][0].replace("/", "-")
    
    def parse_html(self, response):
        """
            This method will help in the decision step of the main parse function in spider class,
            when file is html, return file type as html and return rawContent as encoded for parsing

            Args:
            ---------------------
                response: pass the response returned from the scraper request

            Return:
            ---------------------
                item: returns the items with additional info provided inside
        """
        item = response.meta["item"]
        item["fileType"] = "html"
        item["rawContent"] = response.text.encode()
        yield item
    
    def parse_binary(self, response):
        """
            This method will help in the decision step of the main parse function in spider class,
            when file is pdf, doc, or docx, return file type as binary and return rawContent to pass to MinIO upload

            Args:
            ---------------------
                response: pass the response returned from the scraper request

            Return:
            ---------------------
                item: returns the items with additional info provided inside
        """
        item = response.meta["item"]
        item["fileType"] = "binary"
        item["rawContent"] = response.body
        yield item    