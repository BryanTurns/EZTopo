from ultralytics import YOLO
import cv2
import os

REGENERATE_FRAMES = True
FRAME_CT = 150
MODEL_SIZE = "s"
VID_PATH = "./data/bouldering.MP4"
FRAME_PATH = "./data/frames"
FRAME_TIME_INTERVAL = 2
OUTPUT_VIDEO_PATH = "output.mp4"
OUTPUT_PICTURE_PATH = "output.jpg"
# results = model(["./data/0.jpg", "./data/2.jpg", "./data/3.jpg", "./data/4.jpg", "./data/4.jpg", "./data/5.jpg"])





def main():
    # If the frames need to be regenerated
    if REGENERATE_FRAMES:
        # Regenerate the frames
        n = getFrames()
    else:
        # Check how many frames exist and count
        files = os.listdir(FRAME_PATH)
        n = 0
        for file in files:
            n = n+1
    # Load the model
    model = YOLO(f"./models/yolo11{MODEL_SIZE}-pose.pt")
    # Predict body position from frames
    results = model(genFramePaths(n))

    # prediction data structure: https://stackoverflow.com/questions/75121807/what-are-keypoints-in-yolov7-pose
    # Calculate hip position at each frame 
    hip_pos = []
    for result in results:
        right_hip = result.keypoints.xy[0][11]
        left_hip = result.keypoints.xy[0][12]
        av_x = (right_hip[0] + left_hip[0]) / 2
        av_y = (right_hip[1] + left_hip[1]) / 2
        hip_pos.append((int(av_x), int(av_y)))
    # Load the first frame and write the hip path onto it
    res_img = cv2.imread("./data/frames/frame0.jpg")
    for i in (range(len(hip_pos) - 1)):
        res_img = cv2.line(res_img, hip_pos[i], hip_pos[i+1], (0, 0, 255), 2)
    # Save the image with the hip path
    cv2.imwrite(OUTPUT_PICTURE_PATH, res_img)
    # Overlay hip path on video
    overlayOnVideo(hip_pos)
    


def overlayOnVideo(hip_pos):
    # Load the original video
    cap = cv2.VideoCapture(VID_PATH)
    # Get the fps of the original video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # Get the dimensions of the original video
    dimensions = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # Create and open a video to write the new frames to
    output = cv2.VideoWriter(OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, dimensions)
    
    # For each frame, overlay the hip path onto that frame
    while True:
        # Read a frame from the original video
        success, frame = cap.read()
        # If there are no more frames, exit
        if not success:
            break
        # Overlay the hip path on the frame
        for i in (range(len(hip_pos) - 1)):
            frame = cv2.line(frame, hip_pos[i], hip_pos[i+1], (0, 0, 255), 2)
        # Write the new frame to the output video
        output.write(frame)
    
    cap.release()
    output.release()

def genFramePaths(n):
    name_array = []
    for i in range(n):
        name_array.append(f"./data/frames/frame{i}.jpg");
    return name_array


def getFrames():
    # Open the input video
    vidObj = cv2.VideoCapture(VID_PATH)

    # Remove any files in the frames folder
    files = os.listdir(FRAME_PATH)
    for file in files:
        os.remove(f"./{FRAME_PATH}/{file}")

    # Get the fps of the original video
    fps =  int(vidObj.get(cv2.CAP_PROP_FPS))
    # Calculate how often to take a frame
    frameCaptureInterval = int(FRAME_TIME_INTERVAL * fps)
    # Save every frameCaputreInterval frames
    n = 0
    success = True
    while success:
        # Read a frame
        success, image = vidObj.read()
        # Every frameCaptureInterval, save the frame to the frames folder
        if (n % frameCaptureInterval) == 0:
            cv2.imwrite(f"./{FRAME_PATH}/frame{int(n / frameCaptureInterval)}.jpg", image)
        n = n + 1
    # Close the original video
    vidObj.release()
    # Return how many frames were captured
    return int(n/frameCaptureInterval)

if __name__ == '__main__':
    main()