# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Mentioned in assessment 
    Id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    fileLink = scrapy.Field()
    partition_date = scrapy.Field()

    # Added for clarity
    sourceURL = scrapy.Field()
    documentURL = scrapy.Field()
    fileType = scrapy.Field()
    filePath = scrapy.Field()
    fileHash = scrapy.Field()

    # To pass file contact (binary to the pipeline)
    rawContent = scrapy.Field()

