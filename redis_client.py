import redis
import json
from logger_config import CustomLogger

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
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
        存储论文数据并设置过期时间
        
        Args:
            papers: 论文数据列表
            expire_time: 过期时间（秒），默认172800秒（2天）
        """
        self.logger.info(f"Setting papers with expire time: {expire_time} seconds")
        try:
            self.r.setex(
                paper['link'],          # 键
                expire_time,          # 过期时间（秒）
                json.dumps(paper)     # 值
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


