"""Token Bucket Class"""
from src.util.redis import RedisClient
import os
import time


def refresh_tokens() -> None:
    """refresh tokens"""
    redis = RedisClient().get_client()
    refill_interval = int(os.getenv("BUCKET_REFILL_INTERVAL"))
    refill_size = int(os.getenv("BUCKET_REFILL_SIZE"))
    t = int(refill_interval)
    while True:
        time.sleep(1)
        t = t - 1
        if t == 0:
            if int(redis.get("BUCKET_SIZE")) < (
                int(os.getenv("BUCKET_SIZE")) - refill_size
            ):
                redis.set("BUCKET_SIZE", (int(redis.get("BUCKET_SIZE")) + refill_size))
            t = refill_interval


class TokenBucket:
    """Token Bucket"""

    def __init__(self) -> None:
        """Init"""
        self.redis = RedisClient().get_client()
        self.redis.set("BUCKET_SIZE", os.getenv("BUCKET_SIZE"))

    def set_tokens(self, count):
        """Set tokens"""
        self.redis.set("BUCKET_SIZE", count)

    def get_token_count(self) -> int:
        """get token count"""
        return int(self.redis.get("BUCKET_SIZE"))

    def reduce_token(self):
        """reduce token count"""
        current_token_count = self.get_token_count() - 1
        self.set_tokens(current_token_count)
