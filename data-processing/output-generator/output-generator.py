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
    uuid = redisClient.blpop("outputQueue")[1].decode()
    print("Generating output!")

    jsonBlobName = f"{uuid}.json"
    jsonFilepath = f"{constants['DOWNLOAD_PATH']}/{jsonBlobName}"
    blob = bucket.blob(jsonBlobName)
    blob.download_to_filename(jsonFilepath)

    videoBlobName = f"Upload-{uuid}"
    inputVideoFilepath = f"{constants['DOWNLOAD_PATH']}/{videoBlobName}"
    blob = bucket.blob(videoBlobName)
    blob.download_to_filename(inputVideoFilepath)

    with open(jsonFilepath, "r") as json_file:
        position_data = json.load(json_file)

    inputVideoObject = cv2.VideoCapture(inputVideoFilepath)
    fps = int(inputVideoObject.get(cv2.CAP_PROP_FPS))
    dimensions = (int(inputVideoObject.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoObject.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    outputVideoFilepath = f"{constants['UPLOAD_PATH']}/Output-{uuid}.mp4"
    outputVideoObject = cv2.VideoWriter(outputVideoFilepath, cv2.VideoWriter_fourcc(*'mp4v'), fps, dimensions)

    while True:
        success, inputFrame = inputVideoObject.read()
        if not success:
            break

        for i in range(len(position_data) - 1):
            outputFrame = cv2.line(inputFrame, position_data[i], position_data[i+1], (0, 0, 255), 2)
        outputVideoObject.write(outputFrame)


if __name__ == "__main__":
    main()