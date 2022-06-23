"""Token Bucket Class"""
import os
import time

from src.util.redis import RedisClient

refill_script_lua = open(
    os.path.join(os.path.dirname(__file__), "..", "scripts", "refill-tokens.lua")
)
refill_script = refill_script_lua.read()

BUCKET_SIZE_KEY = "BUCKET_SIZE"
BUCKET_REFILL_INTERVAL_KEY = "BUCKET_REFILL_INTERVAL"
BUCKET_REFILL_SIZE = "BUCKET_REFILL_SIZE"


def refresh_tokens() -> None:
    """refresh tokens"""
    redis = RedisClient().get_client()
    total_bucket_size = int(os.getenv(BUCKET_SIZE_KEY))
    refill_interval = float(os.getenv(BUCKET_REFILL_INTERVAL_KEY))
    refill_size = int(os.getenv(BUCKET_REFILL_SIZE))
    t = float(refill_interval)
    while True:
        time.sleep(t)
        redis.eval(refill_script, 1, BUCKET_SIZE_KEY, total_bucket_size, refill_size)


class TokenBucket:
    """Token Bucket"""

    def __init__(self) -> None:
        """Init"""
        self.redis = RedisClient().get_client()
        self.redis.set(BUCKET_SIZE_KEY, os.getenv(BUCKET_SIZE_KEY))
        self.critical_tokens = round(
            int(os.getenv(BUCKET_SIZE_KEY)) * float(os.getenv("CRITICAL_BUCKET"))
        )

    def set_tokens(self, count):
        """Set tokens"""
        self.redis.set(BUCKET_SIZE_KEY, count)

    def get_token_count(self) -> int:
        """get token count"""
        return int(self.redis.get(BUCKET_SIZE_KEY))

    def reduce_token(self):
        """reduce token count"""
        self.redis.decr(BUCKET_SIZE_KEY, 1)
