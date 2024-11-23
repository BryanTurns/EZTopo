from ultralytics import YOLO
from eztopo_utils.constants import MODEL_SIZE
import cv2

def main():
    model = YOLO(f"./models/yolo11{MODEL_SIZE}-pose.pt")

    