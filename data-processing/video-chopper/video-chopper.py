import cv2, os, redis
from google.cloud import storage
from dotenv import load_dotenv
import threading

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


def  main():
    while True:
        print("Waiting to chop...")
        uuid = redisClient.blpop("chopQueue")[1].decode()
        redisClient.set(uuid, constants["CHOPPING"])
        print(f"Chopping {uuid}")

        blobName = f"Upload-{uuid}"
        blob = bucket.blob(blobName)
        blob.download_to_filename(f"{constants['DOWNLOAD_PATH']}/{blobName}")
        
        videoObject = cv2.VideoCapture(f"{constants['DOWNLOAD_PATH']}/{blobName}")
        fps = int(videoObject.get(cv2.CAP_PROP_FPS))
        # Every frameCaptureInteval seconds, save a frame
        frameCaptureInterval = int(constants["FRAME_TIME_INTERVAL"] * fps)
        n = 0
        success = True
        while success:
            success, image = videoObject.read()
            if (n % frameCaptureInterval) == 0:
                frameNumber = n // frameCaptureInterval
                savePath = f"{constants['UPLOAD_PATH']}/frame-{frameNumber}-{uuid}.jpg"
                cv2.imwrite(savePath, image)
            n = n + 1
        framesCapturedCount = n // frameCaptureInterval
        
        for filename in os.listdir(constants["DOWNLOAD_PATH"]):
            os.remove(f"{constants['DOWNLOAD_PATH']}/{filename}")
        
        threading.Thread(target=upload_frames_to_GCP, args=(uuid, framesCapturedCount)).start()


def upload_frames_to_GCP(uuid, framesCapturedCount):
    print(f"Uploading frames for {uuid}")
    for frameNumber in range(framesCapturedCount):
        blobName = f"frame-{frameNumber}-{uuid}.jpg"
        blob = bucket.blob(blobName)
        blob.upload_from_filename(f"{constants['UPLOAD_PATH']}/{blobName}")
    
    for filename in os.listdir(constants["UPLOAD_PATH"]):
        os.remove(f"{constants['UPLOAD_PATH']}/{filename}")

    redisClient.set(uuid, constants["CHOPPED"])
    redisClient.rpush("predictorQueue", uuid)
    


if __name__ == "__main__":
    main()

