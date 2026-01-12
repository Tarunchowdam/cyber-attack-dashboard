import os
import logging
from app import create_app
from utils.database import db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    try:
        # Connect to MongoDB on startup
        db.connect()
        logger.info("Database connection established")
        
        logger.info(f"Starting Flask server on port {port}")
        logger.info(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
        logger.info(f"Available endpoints:")
        logger.info(f"  - POST /api/register")
        logger.info(f"  - POST /api/login")
        logger.info(f"  - GET  /api/health")
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        db.close()
        raise
    finally:
        # Close database connection on shutdown
        db.close()
        logger.info("Database connection closed")