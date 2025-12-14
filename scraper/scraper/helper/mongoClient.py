from pymongo import MongoClient
import os

class MongoDBClient:
    """
        Mongo will be used as the metadata storage location. 
        This class will help connect to it, upsert metadata, and select data.

    """
    def __init__(self, db_name='Workplacerelation_metadata'):
        """
            Connect to MongoDB service running in Docker.
            The below details in connection are the same as the one defined in docker-compose.yaml
        """
        # The below was added to allow the dubugging of the scrapy module from the terminal
        # and at the same time run it from docker. 
        # The scraper will become enviornment aware
        mongo_host = os.getenv('MONGO_HOST', 'localhost')
        self.client = MongoClient(f"mongodb://{mongo_host}:27017")
        self.db = self.client[db_name]

    def getCollection(self, collectionName):
        """
        Retrieves a collection by name.
        Two collection are used in this assessment:
        - lnd_documents_metadata: stores the metadata of the documents scraped.
        - stg_documents_metadata: stores the transformed metadata of the documents as per requirements.

        Args:
            collectionName: The name of the collection to retrieve.

        Returns:
            Collection: The requested MongoDB collection.
        """
        return self.db[collectionName]

    def upsertItem(self, collectionName, filterQuery, item):
        """
        Upserts an item into the specified collection.

        Args:
            collectionName: The name of the collection to upsert the item into.
            filterQuery: The filter query to find the item to upsert.
            item: The item to upsert.

        Returns:
            None
        """
        collection = self.getCollection(collectionName)
        # Upsert metadata to make sure than when scraping there are no duplicate values in the database
        collection.update_one(filterQuery, {'$set': dict(item)}, upsert=True)

    def finditems(self, collectionName, start_date, end_date):
        """
        Finds items in the specified collection within the given date range.

        Args:
            collectionName: The name of the collection to find items in.
            start_date: The start date of the date range.
            end_date: The end date of the date range.
        Returns:
            list: A list of items found in the collection within the date range.
        """
        collection = self.getCollection(collectionName)
        query = {
            'date': {
                '$gte': start_date,
                '$lte': end_date
            }
        }
        items = list(collection.find(query))
        return items

    def get_database(self, db_name):
        """
        Retrieves a database by name.

        Args:
            db_name (str): The name of the database to retrieve.

        Returns:
            Database: The requested MongoDB database.
        """
        return self.client[db_name]
    
    def close(self):
        """
        Closes the MongoDB client connection.
        """
        self.client.close()