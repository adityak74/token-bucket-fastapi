from fastapi import FastAPI, Request, Response
import time
import dotenv
from src.token_bucket import TokenBucket, refresh_tokens
import multiprocessing

dotenv.load_dotenv()
app = FastAPI()
token_bucket = TokenBucket()
multiprocessing.Process(target=refresh_tokens).start()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    if token_bucket.get_token_count() < 1:
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
