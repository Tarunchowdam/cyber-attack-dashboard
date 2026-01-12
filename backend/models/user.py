from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from utils.database import db
import logging

logger = logging.getLogger(__name__)

class User:
    collection_name = 'users'
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    @staticmethod
    def get_collection():
        """Get users collection"""
        return db.get_collection(User.collection_name)
    
    def save(self):
        """
        Save user to database
        Returns: True if successful, False if email already exists
        """
        try:
            collection = self.get_collection()
            
            # Check if email already exists
            existing_user = collection.find_one({'email': self.email})
            if existing_user:
                logger.warning(f"User with email {self.email} already exists")
                return False
            
            # Hash password before saving
            hashed_password = generate_password_hash(self.password)
            
            # Create user document with only email and password
            user_doc = {
                'email': self.email,
                'password': hashed_password
            }
            
            result = collection.insert_one(user_doc)
            logger.info(f"User created with ID: {result.inserted_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving user: {e}")
            raise
    
    @staticmethod
    def authenticate(email, password):
        """
        Authenticate user with email and password
        Returns: User object if authenticated, None otherwise
        """
        try:
            collection = User.get_collection()
            user = collection.find_one({'email': email})
            
            if user and check_password_hash(user['password'], password):
                logger.info(f"User {email} authenticated successfully")
                return {
                    'email': user['email'],
                    '_id': str(user['_id'])
                }
            
            logger.warning(f"Authentication failed for email: {email}")
            return None
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        try:
            collection = User.get_collection()
            user = collection.find_one({'email': email})
            if user:
                return {
                    'email': user['email'],
                    '_id': str(user['_id'])
                }
            return None
        except Exception as e:
            logger.error(f"Error finding user by email: {e}")
            return None
    
    @staticmethod
    def email_exists(email):
        """Check if email already exists in database"""
        try:
            collection = User.get_collection()
            user = collection.find_one({'email': email})
            return user is not None
        except Exception as e:
            logger.error(f"Error checking if email exists: {e}")
            return False