import redis
import json
from config import REDIS_HOST, REDIS_PORT
from utils import CustomLogger

class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=0):
        self.logger = CustomLogger()
        self.logger.info(f"Initializing Redis client with host={host}, port={port}, db={db}")
        try:
            self.r = redis.Redis(host=host, port=port, db=db)
            self.logger.info("Successfully connected to Redis")
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            raise

    def set(self, key, value):
        try:
            self.r.set(key, value)
            self.logger.debug(f"Successfully set key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to set key {key}: {e}")
            raise

    def get(self, key):
        try:
            value = self.r.get(key)
            self.logger.debug(f"Retrieved value for key: {key}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get key {key}: {e}")
            raise
    
    def set_paper(self, paper, expire_time=172800):
        """
        Save paper data and set expiration time
        
        Args:
            paper: data of a paper
            expire_time: expiration time (seconds), default 172800 seconds (2 days)
        """
        self.logger.info(f"Setting papers with expire time: {expire_time} seconds")
        try:
            self.r.setex(
                paper['link'],          # key
                expire_time,          # expiration time (seconds)
                json.dumps(paper)     # value
            )
            self.logger.debug(f"Stored paper with ID: {paper['link']}")
        except Exception as e:
            self.logger.error(f"Failed to store paper: {e}")
            raise

    def get_paper(self, link):
        self.logger.debug(f"Attempting to retrieve paper with ID: {link}")
        try:
            data = self.get(link)
            if data:
                paper = json.loads(data)
                self.logger.debug(f"Successfully retrieved paper with ID: {link}")
                return paper
            self.logger.info(f"No paper found with ID: {link}")
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving paper with ID {link}: {e}")
            raise


