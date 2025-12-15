FROM python:3.11-slim

# Set Up Scrapy project Root 
WORKDIR /app/scraper
# Will be used to install dependencies
COPY requirements.txt .
# Install libraries
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper/ .

CMD ["bash"]