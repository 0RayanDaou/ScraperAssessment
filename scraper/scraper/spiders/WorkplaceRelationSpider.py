import scrapy as sp
from pathlib import Path
from scraper.helper.HelperFunction import HelperFunction
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin
from scraper.items import ScraperItem

class WorkplaceRelationSpider(sp.Spider):
    """
    This Scraper will be used to scrape the webpage provided in the assessment
    Unique Name: documents
    Way it works:
        Spider → yields Request → Scheduler → Downloader → Response → callback
    """
    # Unique name of the spider
    name = 'documents'
    allowed_domains = ['www.workplacerelations.ie', 'workplacerelations.ie']

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
        self.body = body
        now = datetime.now()
        # Format the datetime object into the specified string format
        logFileName = 'Scraping_' + now.strftime('%Y%m%d%H%M%S') + '_Log.txt'
        # Construct Log File Name Timestamp For different Runs Monitoring
        logFileName = Path('Log') / logFileName
        # Initialize helper class that will help construct urls based on inputs provided
        self.helperClass = HelperFunction(logFileFullPath = logFileName, loggerLevel='DEBUG')
        # hold urls to be called by scraper
        self.urls = self.helperClass.constructScrapingList(start_date=start_date, end_date=end_date, query=query, body=self.body, partition=partition)
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
        i = 0
        # For each url constructed in helper class constructScrapingList yiel request
        self.helperClass.logAction('info', 'Start requests', 'Traversing through requests started.')
        for url in self.urls:
            i += 1
            self.helperClass.logAction('info', 'Initaite reqeusts', 'Request ' + str(i) + ': ' + str(url))
            yield sp.Request(url=url, callback=self.parse, meta={'partition_date': self._extract_partition(url)})

    def parse(self, response):
        """
            Parses the response retrievd from each url. 
            Fields in ScraperItems: Id, title, description, date, partition_date, sourceURL, documentURL, fileType, filePath, fileHash

            Args:
            ---------------------
                response: Url request response
                parition_date: The date retrieved from the from section of the url
                
            Returns:
            ---------------------
                None
        """
        # For every item found in the response page
        # path to items: <div> -> <ul> -> <li class="each-item>
        # Css can find class directly with no need to move through paths
        self.helperClass.logAction('info', 'Parse Response', 'parsing responses started, items extraction in progress.')
        listOfItems = response.css('li.each-item')
        for row in listOfItems:
            # Initialize item
            item = ScraperItem()
            # Populate item
            item['Id'] = row.css('span.refNO::text').get()
            item['title'] = row.css('h2.title a::text').get()
            item['description'] = row.css('p.description::text').get()
            item['date'] = row.css('span.date::text').get()
            item['partition_date'] = response.meta['partition_date']
            item['sourceURL'] = response.url
            documentURL = str(urljoin(response.url, row.css('h2.title a::attr(href)').get()))
            item['documentURL'] = documentURL
            item['body'] = self.body.replace(',', '-')
            
            # Decision step to perform requirements as provided in assesment
            # If pdf, doc, docx then call parse_binary
            if documentURL.endswith(('.pdf', '.doc', '.docx')):
                yield response.follow(documentURL,callback=self.parse_binary,meta={'item': item})
            # else parse_html
            else:
                yield response.follow(documentURL,callback=self.parse_html,meta={'item': item})
        # The below logic is for pagination
        # If items exist on this page, try next page
        if listOfItems and len(listOfItems) > 0:
            current_page = response.meta.get('pageNumber', 1)
            # After receiving the items of first page, increment page number by 1
            next_page = current_page + 1

            # If pageNumber in request then remove pageNumber to add new one
            if 'pageNumber=' in response.url:
                base_url = response.url.split('&pageNumber=')[0]
            # If pageNumber not in request then first call the no action
            else:
                base_url = response.url
            # Get url of next page
            next_page_url = f"{base_url}&pageNumber={next_page}"

            self.helperClass.logAction('info', 'Pagination', f'Following pageNumber={next_page}'
            )
            
            yield response.follow(next_page_url,callback=self.parse,meta={'partition_date': response.meta['partition_date'],'pageNumber': next_page})

        self.helperClass.logAction('info', 'Parse Response', 'Parsing responses finished, items extraction is finalized.')

    def _extract_partition(self, url):
        """
            Extracts the 'from' date from the url.

            Args:
            ---------------------
                url: the url used to extratc the date from
            
            Returns:
            ---------------------
                date: date string with format dd-MM-YYYY Ex: 04-11-2025

        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        paritionDate = params['from'][0].replace('/', '-')
        self.helperClass.logAction('info', 'Parition Date', 'Parition Date Extracted: ' + str(paritionDate))
        # take the "from" date as the partition identifier
        return paritionDate
    
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
        self.helperClass.logAction('info', 'Parse HTML File', 'HTML File Detected.')
        item = response.meta['item']
        item['fileType'] = 'html'
        item['rawContent'] = response.text.encode()
        yield item

        links = response.css('a::attr(href)').getall()

        for href in links:
            if href.lower().endswith(('.pdf', '.doc', '.docx')):
                yield response.follow(href, callback=self.parse_binary, meta={'item': item.copy()})
    
    def parse_binary(self, response):
        """
            This method will help in the decision step of the main parse function in spider class,
            when file is pdf, doc, or docx, set file type as file extension and return rawContent to pass to MinIO upload

            Args:
            ---------------------
                response: pass the response returned from the scraper request

            Return:
            ---------------------
                item: returns the items with additional info provided inside
        """
        self.helperClass.logAction('info', 'Parse PDF, Docx, Doc File', 'PDF, Doc, or Docx File Detected.')
        item = response.meta['item']
        item['fileType'] = response.url.split('.')[-1].lower()
        item['rawContent'] = response.body
        yield item    