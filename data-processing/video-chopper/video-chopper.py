import cv2, os, redis
from google.cloud import storage
from dotenv import load_dotenv

print("Loading environment variables")
load_dotenv("../../.env")
constants = {"BUCKET_NAME": os.getenv("BUCKET_NAME"),
             "DOWNLOAD_PATH": "./data/input",
             "UPLOAD_PATH": "./data/output",
             "FRAME_TIME_INTERVAL": 2}

print("Initiating Redis")
redisClient = redis.Redis(host="localhost", port=6379)

print("Initiating storage")
storage_client = storage.Client()
bucket = storage_client.bucket(constants["BUCKET_NAME"])


def  main():
    while True:
        print("Waiting for work...")
        uuid = redisClient.blpop("chopQueue")[1].decode()
        print("Working!")

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
        
        dataFiles = os.listdir(constants["DOWNLOAD_PATH"])
        for filename in dataFiles:
            os.remove(f"{constants['DOWNLOAD_PATH']}/{filename}")

        
        
        




    


if __name__ == "__main__":
    main()

