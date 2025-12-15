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
Scrapy will be responsible of:
- Web scraping of Workplace Relation documents (https://www.workplacerelations.ie). 
- Pagination
- Parsing/Extracting metadata
- Downloading documents
- Passing structure items to pipelines

To start a scrapy project:
  - scrapy startproject projectName

#### scrapy.cfg
scrapy.cfg is the entry point configuration file for Scrapy.
It defines:
 - The default Scrapy settings module
 - The project name
 - How Scrapy commands resolve the project
This allows running commands like:
 - scrapy crawl documents

#### WorkplacerelationSpider.py
This is the spider that constructs requests, parses results, follow document links, and pass metadata.

#### item.py
Define the schema of a scraped document
Example fields:
 - Id
 - title
 - description
 - date
 - partition_date
 - sourceURL
 - documentURL
 - fileType
 - rawContent
 - filePath
 - fileHash

#### pipelines.py
Pipelines are responsible for post-processing scraped items. 
Several actions happen within:
 - Get SHA-256 hash of file content
 - Upload file to MinIO (landing bucket)
 - Store metadata in MongoDB
 - Perform upsert acts on MongoDB

#### mongoClient.py
Connects to MongoDB and allows receiving and sending data. 
Used to store metadata of scraped data:
 - lnd_documents_metadata -> raw scraped metadata
 - stg_documents_metadata -> transformed metadata
MongoDB run as a docker service.

#### minioClient.py
Connects to MinIO for object download and upload.
Used to store objects/files:
 - landing -> raw files from scraping
 - staging -> transformed files
MinIO runs as a Docker service and includes a web console.

#### HelperFunction.py
Common functions used in scraper and transform classes.
Responsibilities:
 - Logging
 - URL Construction

#### Logger.py
Custom Logger class. 
Used to create and log steps into a log file

#### transform.py
This applies to second part of assignment:
 - Fetch data from landing Metadata Layer
 - Downloads corresponding files from MinIO
 - Applies logic based on file Type:
 	- PDF / DOC / DOCX -> no content change
	- HTML -> cleaned using BeautifulSoup
 - Recalculation of hash
 - Rename files
 - Upload to staging bucket
 - Upsert metadata to stg_documents_metadata with new file location, hash, and name

