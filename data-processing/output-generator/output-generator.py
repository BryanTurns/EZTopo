import cv2, os, redis
from google.cloud import storage
from dotenv import load_dotenv

print("Loading environment variables")
load_dotenv("../../.env")
constants = {"BUCKET_NAME": os.getenv("BUCKET_NAME"),
             "DOWNLOAD_PATH": "./data/input",
             "UPLOAD_PATH": "./data/output",
             "FRAME_TIME_INTERVAL": 2,
             "CHOPPING": os.getenv("CHOPPING"),
             "CHOPPED": os.getenv("CHOPPED")}

print("Initiating Redis")
redisClient = redis.Redis(host="localhost", port=6379)

print("Initiating storage")
storage_client = storage.Client()
bucket = storage_client.bucket(constants["BUCKET_NAME"])

def main():
    pass

if __name__ == "__main__":
    main()