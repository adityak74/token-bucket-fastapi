import os

import redis


class RedisClient:
    """Redis Client Class"""

    def __init__(self) -> None:
        """Redis client init"""
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_port = os.getenv("REDIS_PORT")

    def get_client(self) -> redis.Redis:
        """Get client"""
        return redis.Redis(host=self.redis_host, port=self.redis_port)
