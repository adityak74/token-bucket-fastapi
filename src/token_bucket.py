"""Token Bucket Class"""
import os
import time

from src.util.redis import RedisClient


def refresh_tokens() -> None:
    """refresh tokens"""
    redis = RedisClient().get_client()
    total_bucket_size = int(os.getenv("BUCKET_SIZE"))
    refill_interval = int(os.getenv("BUCKET_REFILL_INTERVAL"))
    refill_size = int(os.getenv("BUCKET_REFILL_SIZE"))
    t = int(refill_interval)
    while True:
        time.sleep(1)
        t = t - 1
        if t == 0:
            current_bucket_size = int(redis.get("BUCKET_SIZE"))
            if current_bucket_size < (total_bucket_size - refill_size):
                pipe = redis.pipeline()
                pipe.multi()
                if current_bucket_size <= 0:
                    pipe.set("BUCKET_SIZE", total_bucket_size)
                else:
                    pipe.set("BUCKET_SIZE", int(current_bucket_size) + refill_size)
                pipe.execute()
            t = refill_interval


class TokenBucket:
    """Token Bucket"""

    def __init__(self) -> None:
        """Init"""
        self.redis = RedisClient().get_client()
        self.redis.set("BUCKET_SIZE", os.getenv("BUCKET_SIZE"))
        self.critical_tokens = round(
            int(os.getenv("BUCKET_SIZE")) * float(os.getenv("CRITICAL_BUCKET"))
        )

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
