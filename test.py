import scrapy
from pathlib import Path
from scraper.scraper.helper.HelperFunction import HelperFunction
from scraper.scraper.spiders.WorkplaceRelationSpider import WorkplaceRelationSpider




def hey():
    hc = HelperFunction('','C:\\Users\\Brother\\Desktop\\Kedra\\Scraping\\ScraperAssessment\\Logs\\Log_12345.txt', 'DEBUG')

    urls = hc.constructScrapingList('4/11/2025', '1/12/2025', 'labour', 'Labour Count,Workplace Relations Commission', 10)

    print(urls)
    # Spider → yields Request → Scheduler → Downloader → Response → callback
    def parse(response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)

    z = scrapy.Request(url='https://www.workplacerelations.ie/en/search/?decisions=1&q=%22labour%22&from=04/11/2025&to=14/11/2025&body=3,15376', callback=parse)

    print(scrapy.downloadermiddlewares)
