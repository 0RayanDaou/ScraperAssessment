# ScraperAssessment
The following is a repository that holds the solution developed for the Web Scraper Assessment requested by Kedra.

## Overview
This project is an end-to-end document ingestion and transformation pipeline built using:
 - Scrapy
 - Docker
 - MongoDB
 - MinIO

### Scrapy:
Web scraping of Workplace Relation documents (https://www.workplacerelations.ie). 
To start a scrapy project:
  - scrapy startproject projectName
SCRAPERASSESSMENT/
 scraper/
   scrapy.cfg
   	scraper/
        spiders/
       	WorkplaceRelationSpider.py
        exception/
       	Exception.py
        helper/
       	HelperFunction.py
	    mongoClient.py
            minioClient.py
        logger/
            Logger.py
        transformation/
            transform.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
 Dockerfile
 docker-compose.yaml
 requirements.txt















































