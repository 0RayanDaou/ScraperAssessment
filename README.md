# ScraperAssessment
The following is a repository that holds the solution developed for the Web Scraper Assessment requested by Kedra.

## Overview
This project is an end-to-end document ingestion and transformation pipeline built using:
 - Scrapy -- Web Scraping and Parsing
 - Docker -- Containerization/Execution
 - MongoDB -- Metadata Storage
 - MinIO -- Object Storage

Two layers are used:
 - Scraping (Landing Layer)
 - Transformation (Staging Layer)

## Project Structure
- SCRAPERASSESSMENT
	-  scraper/
 		-  scrapy.cfg
   		- scraper/
     		- spiders/
       		- WorkplaceRelationSpider.py
         	- exception/
          		- Exception.py
            - helper/
            	- HelperFunction.py
             	- mongoClient.py
              	- minioClient.py
          	- logger/
          		- Logger.py
          	 - transformation/
          	 	- transform.py
       - items.py
       - middlewares.py
       - pipelines.py
       - settings.py
	- Dockerfile
 	- docker-compose.yaml
  	- requirements.txt

### Scrapy:
Web scraping of Workplace Relation documents (https://www.workplacerelations.ie). 
To start a scrapy project:
  - scrapy startproject projectName















































