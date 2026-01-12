from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Connect to MongoDB"""
        if self._client is None:
            try:
                mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/cyber_dashboard')
                logger.info(f"Connecting to MongoDB...")
                self._client = MongoClient(mongo_uri)
                self._db = self._client.get_database()
                logger.info("Successfully connected to MongoDB")
                
                # Test connection
                self._db.command('ping')
                logger.info("MongoDB ping successful")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise
        return self._db
    
    def get_db(self):
        """Get database instance"""
        if self._db is None:
            return self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        db = self.get_db()
        return db[collection_name]
    
    def close(self):
        """Close MongoDB connection"""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")

# Global database instance
db = Database()