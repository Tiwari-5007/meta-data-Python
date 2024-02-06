import redis
import re
import azureFileHandler as az
from dotenv import load_dotenv
import os
from logsHandler import logw
import utils as sendreq
# Load environment variables from .env
load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))

# Config :- Needs to be added later.
def get_redis():
    try:
        redis_conn = redis.StrictRedis(host=redis_host, port=redis_port)
        if redis_conn.ping():
            return redis_conn
    except Exception as e:
        return None
        print(e)
        #logger.warning(f"{stamp()} Redis connection failed: {str(e)}")

def get_all_keys(redis_conn):
    keys = []
    for key in redis_conn.keys(b"*.*_*_*_*"):
        key.decode('utf-8')
        if re.match(rb'\d+\.\d+_\d+_file_trnsfr',key):
            keys.append(key)
    return keys


def process_redis_key_data(redis_conn, key):
    try:
        if redis_conn and key:
            data = redis_conn.get(key)
            decoded_data = data.decode("utf-8")
            #print(f"Key:{key} and value:{decoded_data}")
            logw("info", f"Processing {key}: With Data: {decoded_data}")
            if decoded_data is not None:
                mon_file_name = decoded_data.split("##")[0]
                mon_file_path = decoded_data.split("##")[1]
                if mon_file_name and mon_file_path:
                    logw("info", f"Deleting The key {key}")
                    redis_conn.delete(key)
                    az.handle_data(mon_file_name,mon_file_path)
                    sendreq.sendmetaData(decoded_data)
            else:
                logw("warning", f"For {key}: No Data Found")
                # print("Log that For particular key data not found")
                # Log that For particular key data not found
    except Exception as e:
        print(e)
