import cv2, hashlib, os
from time import sleep


LOCAL = True
LOCAL_VID_PATH = "../../local-data/input/bouldering.MP4"
LOCAL_FRAME_PATH = "../../local-data/frames/"
# Number of seconds between saved frames
FRAME_TIME_INTERVAL = 2

def main():
    while True:
        if LOCAL:
            vidObj = getVideoLocal(LOCAL_VID_PATH)
            vidHash = generate_fingerprint(LOCAL_VID_PATH, 10)
            files = os.listdir(LOCAL_FRAME_PATH)
            for file in files:
                os.remove(f"./{LOCAL_FRAME_PATH}/{file}")

        fps = int(vidObj.get(cv2.CAP_PROP_FPS))
        # Every frameCaptureInteval, save a frame
        frameCaptureInterval = int(FRAME_TIME_INTERVAL * fps)
        # Number of frames read
        n = 0
        success = True
        while success:
            # Read a frame
            success, image = vidObj.read()
            # Every frameCaptureInterval, save the frame
            if (n % frameCaptureInterval) == 0:
                if LOCAL:
                    savePath = LOCAL_FRAME_PATH + f"{vidHash}-frame{n // frameCaptureInterval}.jpg"
                    saveVideoLocal(savePath, image)
            n = n + 1


        if LOCAL:
            break


def saveVideoLocal(path, img):
    cv2.imwrite(path, img)


def getVideoLocal(path):
    vidObj = cv2.VideoCapture(path)

    return vidObj


# Generated from chatgpt
# Generates hash based on first n chunks. If n < 0 then do the whole file
def generate_fingerprint(file_path, n):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        if n > 0:
            for i in range(n):
                chunk = file.read(4096)  # Read file in chunks
                if not chunk:
                    break
                hasher.update(chunk)
        else:
            while True:
                chunk = file.read(4096)  # Read file in chunks
                if not chunk:
                    break
                hasher.update(chunk)
    return hasher.hexdigest()

if __name__ == "__main__":
    main()

