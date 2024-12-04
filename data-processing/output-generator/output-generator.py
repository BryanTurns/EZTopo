import cv2, os, redis, json
from google.cloud import storage

def getKey():
    with open("/etc/secret-volume/service-account", "r") as secretFile:
        secretData = secretFile.read()
    with open("./key.json", "w+") as keyFile:
        keyFile.write(secretData)

print("Loading environment variables")
constants = {"BUCKET_NAME": "eztopo-bucket",
             "DOWNLOAD_PATH": "./data/input",
             "UPLOAD_PATH": "./data/output",
             "FRAME_TIME_INTERVAL": 2,
             "GENERATING_OUTPUT": 8,
             "GENERATED_OUTPUT": 9,
             "REDIS_HOST": "10.108.148.45",
             "REDIS_PORT": 6379}

print("Initiating Redis")
redisClient = redis.Redis(host=constants["REDIS_HOST"], port=constants["REDIS_PORT"])

print("Initiating storage")
getKey()
storage_client = storage.Client.from_service_account_json("./key.json")
bucket = storage_client.bucket(constants["BUCKET_NAME"])

def main():
    while True:
        print("Waiting to generate output...")
        uuid = redisClient.blpop("outputQueue")[1].decode()
        redisClient.set(uuid, constants["GENERATING_OUTPUT"])
        print("Generating output!")

        jsonBlobName = f"{uuid}.json"
        jsonFilepath = f"{constants['DOWNLOAD_PATH']}/{jsonBlobName}"
        jsonBlob = bucket.blob(jsonBlobName)
        jsonBlob.download_to_filename(jsonFilepath)

        videoBlobName = f"Upload-{uuid}"
        inputVideoFilepath = f"{constants['DOWNLOAD_PATH']}/{videoBlobName}"
        videoInputBlob = bucket.blob(videoBlobName)
        videoInputBlob.download_to_filename(inputVideoFilepath)

        with open(jsonFilepath, "r") as json_file:
            position_data = json.load(json_file)

        inputVideoObject = cv2.VideoCapture(inputVideoFilepath)
        fps = int(inputVideoObject.get(cv2.CAP_PROP_FPS))
        dimensions = (int(inputVideoObject.get(cv2.CAP_PROP_FRAME_WIDTH)), int(inputVideoObject.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        outputVideoFilepath = f"{constants['UPLOAD_PATH']}/Output-{uuid}.mp4"
        outputVideoObject = cv2.VideoWriter(outputVideoFilepath, cv2.VideoWriter_fourcc(*'avc1'), fps, dimensions)

        while True:
            success, inputFrame = inputVideoObject.read()
            if not success:
                break

            for i in range(len(position_data) - 1):
                outputFrame = cv2.line(inputFrame, position_data[i], position_data[i+1], (0, 0, 255), 2)
            outputVideoObject.write(outputFrame)
        inputVideoObject.release()
        outputVideoObject.release()

        outputBlobName = f"Output-{uuid}.mp4"
        blob = bucket.blob(outputBlobName)
        blob.upload_from_filename(outputVideoFilepath)

        redisClient.set(uuid, constants["GENERATED_OUTPUT"])

        os.remove(jsonFilepath)
        os.remove(inputVideoFilepath)
        os.remove(outputVideoFilepath)
        videoInputBlob.delete()
        jsonBlob.delete()

if __name__ == "__main__":
    main()