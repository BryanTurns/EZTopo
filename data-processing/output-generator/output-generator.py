import cv2, os, redis, json
from google.cloud import storage
from dotenv import load_dotenv

print("Loading environment variables")
load_dotenv("../../.env")
constants = {"BUCKET_NAME": os.getenv("BUCKET_NAME"),
             "DOWNLOAD_PATH": "./data/input",
             "UPLOAD_PATH": "./data/output",
             "FRAME_TIME_INTERVAL": 2,}

print("Initiating Redis")
redisClient = redis.Redis(host="localhost", port=6379)

print("Initiating storage")
storage_client = storage.Client()
bucket = storage_client.bucket(constants["BUCKET_NAME"])

def main():
    print("Waiting to generate output...")
    uuid = redisClient.blpop("outputQueue").decode()
    print("Generating output!")

    blobName = f"{uuid}.json"
    json_filepath = f"{constants["DOWNLOAD_PATH"]}/{blobName}"
    blob = bucket.blob(blobName)
    blob.download_to_filename(json_filepath)

    with open(json_filepath, "r") as json_file:
        position_data = json.load(json_file)
    print(position_data)





    pass

if __name__ == "__main__":
    main()