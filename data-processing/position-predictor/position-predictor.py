from ultralytics import YOLO
from dotenv import load_dotenv
from google.cloud import storage
import cv2, os, redis, threading

# print("Loading environment variables")
# load_dotenv("../../.env")
# constants = {"BUCKET_NAME": os.getenv("BUCKET_NAME"),
#              "DOWNLOAD_PATH": "./data/input",
#              "UPLOAD_PATH": "./data/output",
#              "FRAME_TIME_INTERVAL": 2,
#              "PREDICTING": os.getenv("PREDICTING"),
#              "PREDICTED": os.getenv("PREDICTED")}
constants = {"BUCKET_NAME": "eztopo-bucket",
             "PREDICTING": 6,
             "PREDICTED": 7,
             "DOWNLOAD_PATH": "./data/input",
             "UPLOAD_PATH": "./data/output"}

print("Initiating Redis")
redisClient = redis.Redis(host="localhost", port=6379)

print("Initiating storage")
storage_client = storage.Client()
bucket = storage_client.bucket(constants["BUCKET_NAME"])

print("Loading model")
model = YOLO(f"./models/yolo11s-pose.pt")

def main():
    while True:
        

        print("Waiting to predict...")
        data = redisClient.blpop("predictorQueue")[1].decode().split(" ")
        uuid = data[0]
        framesCapturedCount = int(data[1])
        redisClient.set(uuid, constants["PREDICTING"])
        print(f"Predicting for {uuid}")

        threading.Thread(target=predictor_work, args=(uuid, framesCapturedCount)).start()

def predictor_work(uuid, framesCapturedCount):
    blobNames = []
    for frameNumber in range(framesCapturedCount):
        blobNames.append(f"frame-{frameNumber}-{uuid}.jpg")
        blob = bucket.blob(blobNames[frameNumber])
        # with open(f"{constants['DOWNLOAD_PATH']}/{blobNames[frameNumber]}", "wb+") as currentFrameFile:
        blob.download_to_filename(f"{constants['DOWNLOAD_PATH']}/{blobNames[frameNumber]}")
    
        

if __name__ == "__main__":
    main()
    