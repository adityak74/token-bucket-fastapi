import multiprocessing
import time
import logging
import dotenv
from fastapi import FastAPI, Request, Response

from src.token_bucket import TokenBucket, refresh_tokens

logging.basicConfig(format="%(asctime)s\t%(message)s",filename='token-bucket.log', encoding='utf-8', level=logging.DEBUG)
dotenv.load_dotenv()
app = FastAPI()
token_bucket = TokenBucket()
multiprocessing.Process(target=refresh_tokens).start()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    current_token_count = token_bucket.get_token_count()
    logging.debug(f"{current_token_count}")
    if current_token_count < 1:
        return Response(None, status_code=503)
    # remove a token from bucket
    token_bucket.reduce_token()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def read_root():
    return {"bucket_token_count": token_bucket.get_token_count()}
