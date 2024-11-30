from ultralytics import YOLO
# from dotenv import load_dotenv
from google.cloud import storage
import os, redis, threading, json

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
    localFramePaths = []
    for frameNumber in range(framesCapturedCount):
        frame_filename = f"frame-{frameNumber}-{uuid}.jpg"
        frame_filepath = f"{constants['DOWNLOAD_PATH']}/{frame_filename}"
        
        blob = bucket.blob(frame_filename)
        blob.download_to_filename(frame_filepath)
        localFramePaths.append(frame_filepath)
    
    # prediction data structure: https://stackoverflow.com/questions/75121807/what-are-keypoints-in-yolov7-pose
    results = model.predict(localFramePaths)
    hip_pos = []
    for result in results:
        right_hip = result.keypoints.xy[0][11]
        left_hip = result.keypoints.xy[0][12]
        av_x = (right_hip[0] + left_hip[0]) // 2 
        av_y = (right_hip[1] + left_hip[1]) // 2
        hip_pos.append((int(av_x), int(av_y)))

    hip_pos_json = json.dumps(hip_pos)
    json_filename = f"{uuid}.json"
    json_filepath = f"{constants['UPLOAD_PATH']}/{json_filename}"
    with open(json_filepath, "w+") as json_file:
        json_file.write(hip_pos_json)


    blob = bucket.blob(json_filename)
    blob.upload_from_filename(json_filepath)

    redisClient.set(uuid, constants["PREDICTED"])
    redisClient.rpush("outputQueue", uuid)

    
    


if __name__ == "__main__":
    main()
    