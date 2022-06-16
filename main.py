import uvicorn
import multiprocessing
import logging
import dotenv
import os
from fastapi import FastAPI, Request, Response

from src.token_bucket import TokenBucket, refresh_tokens

logging.basicConfig(
    format="%(asctime)s\t%(message)s",
    filename="token-bucket.log",
    encoding="utf-8",
    level=logging.DEBUG,
)
dotenv.load_dotenv()
app = FastAPI()
token_bucket = TokenBucket()
multiprocessing.Process(target=refresh_tokens).start()
load_shedding = bool(os.getenv("LOAD_SHEDDING"))


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    current_token_count = token_bucket.get_token_count()
    logging.debug(f"{current_token_count}")
    if current_token_count < 1:
        return Response(None, status_code=503)
    # remove a token from bucket
    token_bucket.reduce_token()
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"bucket_token_count": token_bucket.get_token_count()}


@app.get("/load")
def load(q: int):
    # non-critical request
    # logging.debug(f"Checking req load q={str(q)} and load shedding={str(load_shedding)}")
    if load_shedding and q == 0:
        # return http 429 too many requests
        current_token_count = token_bucket.get_token_count()
        if current_token_count <= token_bucket.critical_tokens:
            logging.debug(f"Discarded Non Critical Request")
            return Response(None, status_code=429)
    # for q == 1 those are critical request that are allowed to pass
    return {"bucket_token_count": token_bucket.get_token_count()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
