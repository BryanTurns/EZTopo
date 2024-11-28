import cv2, os, redis
# from google.cloud import storage


redisClient = redis.Redis(host="localhost", port=6379)

def  main():
    while True:
        uuid = redisClient.blpop("chopQueue")[1].decode()
        





    videoObject = cv2.VideoCapture("./input.mp4")

    fps = int(videoObject.get(cv2.CAP_PROP_FPS))
    # Every frameCaptureInteval, save a frame
    frameCaptureInterval = int(constants.FRAME_TIME_INTERVAL * fps)
    # Number of frames read
    n = 0
    success = True
    while success:
        # Read a frame
        success, image = videoObject.read()
        # Every frameCaptureInterval, save the frame
        if (n % frameCaptureInterval) == 0:
            frameNumber = n // frameCaptureInterval
            savePath = f"./data/frame-{frameNumber}-{videoHash}.jpg"
            # Consider changing img quality in params
            cv2.imwrite(savePath, image)
        n = n + 1
    
    # Clear files from data for next call
    dataFiles = os.listdir("./data")
    for file in dataFiles:
        os.remove(f"./data/{file}")


if __name__ == "__main__":
    main()

