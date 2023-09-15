import uvicorn
import logging
import time
from fastapi import FastAPI
from routes.users import route
from requests import Request
import subprocess

app = FastAPI()

logger = logging.getLogger(__name__)
logging.getLogger("watchfiles.main").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filename="logs.txt"
    )

@app.middleware("http")
async def loggingInfo(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(
        f"{request.client} -  method: {request.method} - path: {request.scope['path']} - status_code: {response.status_code} - process_time: {process_time}"
        )
    return response

app.include_router(route)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

'''if __name__ == "__main__":
    cmd = "uvicorn main:app --host 0.0.0.0 --port 7868 --reload &"
    subprocess.Popen(cmd, shell=True)'''

