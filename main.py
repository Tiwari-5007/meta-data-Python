#!/Czentrix/apps/erp_python/venv37/bin/python
import signal
import sys
import time
from fastapi import FastAPI
import redisFileHandler as Redis
import textFileHandler  as txtHan
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables from .env
load_dotenv()

sr_host = os.getenv("SR_HOST") or "127.0.0.1"
sr_port = int(os.getenv("SR_PORT")) or 8000

app = FastAPI()

# Initiates the Service
def my_service():
    # Handle the Service Termination.
    #def signal_handler(signum, frame):
        #print("Received termination signal. Stopping service...")
        #sys.exit(0)

    #signal.signal(signal.SIGINT, signal_handler)

    # Start the Service inside infinite Loop
    while True:
        start_process()
        time.sleep(5)


def start_process():
    redis_conn = Redis.get_redis()
    if redis_conn:
        keys = Redis.get_all_keys(redis_conn)
        print("List of Keys Found",keys)
        if keys:
            for key in keys:
                Redis.process_redis_key_data(redis_conn, key)
    else:
        dataList = txtHan.read_remote_file()
        #dataList = txtHan.read_file_data()
        print("Data from File",dataList)
        if dataList:
            for key in dataList:
                txtHan.process_file_key_data(key)



@app.on_event("startup")
def startup_event():
    my_service()

if __name__ == "__main__":
    # Use the import string for the FastAPI application
    uvicorn.run("main:app", host=sr_host, port=sr_port, reload=True)
