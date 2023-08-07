""" This module defines the AnimalShelter class, which provides an interface
for interacting with an animal shelter MongoDB collection.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import os 
import sys

host = os.environ["MONGO_HOST"]
print('My Mongo server is %s' % host)
port = os.environ["MONGO_PORT"]
print('My Mongo port is %s' % port)

              
class AnimalShelter(object):
    """Represents an interface for interacting with an animal shelter MongoDB 
    collection.

    Parameters:
        user (str): MongoDB username.
        password (str): MongoDB password.
        hostname (str): MongoDB hostname.
        port (int): MongoDB port number.

    Attributes:
        username (str): MongoDB username.
        password (str): MongoDB password.
        hostname (str): MongoDB hostname.
        port (int): MongoDB port number.
        client (MongoClient): MongoDB client object.
        database (MongoClient.database): MongoDB database object.
        collection (MongoClient.database.collection): MongoDB collection object.
    """
    def __init__(self, user, password, hostname, port):
        """Constructor for the AnimalShelter class.

        Args:
            user (str): MongoDB username.
            password (str): MongoDB password.
            hostname (str): MongoDB hostname.
            port (int): MongoDB port number.
        """    
        #Connection Variables
        DB = 'AAC'
        COL = 'animals'
        
        #
        # Initialize Connection
        #
        self.username = user
        self.password = password
        self.hostname = hostname
        self.port = port
        
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (user, password, 
                                                             hostname, port))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]
        
    def connect(self):
        """Connect to the MongoDB database and print the connection details.
        """
        print('Connected to <' + self.hostname + '>')
        print('using ' + self.username + '/' +self.password)     
                                  
    def create(self, data):
        """Create a new document in the MongoDB collection.

        Args:
            data (dict): Data to be inserted.

        Returns:
            bool: True if the document was successfully added, False otherwise.

        Raises:
            Exception: If the data parameter is empty.
        """
        if data is not None:
            self.database.animals.insert_one(data) # Data should be a dictionary
            return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    def read(self, search):
        """Retrieve documents from the MongoDB collection based on the search criteria.

        Args:
            search (dict): Search criteria.

        Returns:
            list: A list containing the matching documents.

        Note:
            An empty list will be returned if the search criteria are not found.
        """
        if search is not None: 
            searchResult = list(self.database.animals.find(search)) 
            return searchResult
        else:
            return [] 

    def update(self, initial, change):
        """Update documents in the MongoDB collection that match the initial query.

        Args:
            initial (dict): Initial query criteria.
            change (dict): Fields to be updated.

        Returns:
            int or str: The number of documents modified if successful, or "No 
            document was found" if no matches.

        Raises:
            Exception: If the data parameter is empty.
        """
        if initial is not None:
            if self.database.animals.count_documents(initial, limit = 1) != 0:
                update_result = self.database.animals.update_many(initial, 
                                                                  {"$set": change})
                result = update_result.modified_count
                print("Finding ", initial ,",updating to", change)
            else:
                result = "No document was found"
            return result
        else:
            raise Exception("Nothing to update, because data parameter is empty")

    def delete(self, remove):
        """Delete documents from the MongoDB collection that match the remove criteria.

        Args:
            remove (dict): Criteria to identify documents to be removed.

        Returns:
            int: The number of documents deleted if successful.

        Raises:
            Exception: If the data parameter is empty or no matching documents are found.
        """
        if remove is not None:
            if self.database.animals.count_documents(remove, limit = 1) != 0:
                delete_result = self.database.animals.delete_many(remove)
                return delete_result.deleted_count
            else:
                raise Exception ("No document was found")
            return result
        else:
            raise Exception("Nothing to delete, because data parameter is empty")
