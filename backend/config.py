import os

# Every intermediate and finished artifact lives under this directory. Mount a
# volume here if you want results to survive the container.
DATA_ROOT = os.environ.get("EZTOPO_DATA_DIR", "/data")
UPLOAD_PATH = os.path.join(DATA_ROOT, "uploads")
FRAME_PATH = os.path.join(DATA_ROOT, "frames")
POSITION_PATH = os.path.join(DATA_ROOT, "positions")
OUTPUT_PATH = os.path.join(DATA_ROOT, "outputs")
WORKING_PATHS = (UPLOAD_PATH, FRAME_PATH, POSITION_PATH, OUTPUT_PATH)

MODEL_PATH = os.environ.get("EZTOPO_MODEL_PATH", "./models/yolo11s-pose.pt")

# Seconds of video between each frame handed to the pose model.
FRAME_TIME_INTERVAL = float(os.environ.get("EZTOPO_FRAME_INTERVAL", "1"))
# How many frames the pose model is given at a time.
PREDICT_BATCH_SIZE = int(os.environ.get("EZTOPO_PREDICT_BATCH", "16"))

MAX_UPLOAD_BYTES = 1000 * 1024 * 1024

# Status codes reported by /api/checkStatus. The frontend maps these to the
# messages in translateStatus(), so they have to stay stable.
UNKNOWN = -1
USER_UPLOAD_INITIATED = 2
USER_UPLOAD_COMPLETE = 3
CHOPPING = 4
CHOPPED = 5
PREDICTING = 6
PREDICTED = 7
GENERATING_OUTPUT = 8
GENERATED_OUTPUT = 9
