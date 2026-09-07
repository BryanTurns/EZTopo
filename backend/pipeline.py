"""The video -> topology pipeline.

This used to be three separate services (video-chopper, position-predictor,
output-generator) passing UUIDs through Redis queues and files through a Google
Cloud Storage bucket. It is now three worker threads in one process passing
UUIDs through queue.Queue and files through a local working directory.

Each stage still runs on its own thread, so one video can be having its path
drawn while the next one is still being chopped.
"""

import json
import os
import queue
import shutil
import subprocess
import threading
from functools import cmp_to_key

import cv2

import config

_chop_queue = queue.Queue()
_predict_queue = queue.Queue()
_output_queue = queue.Queue()

_statuses = {}
_status_lock = threading.Lock()

_model = None

_workers = {}


def set_status(uuid, status):
    with _status_lock:
        _statuses[uuid] = status


def get_status(uuid):
    with _status_lock:
        return _statuses.get(uuid, config.UNKNOWN)


def submit(uuid):
    """Hand a freshly uploaded video to the first stage."""
    _chop_queue.put(uuid)


def upload_path(uuid):
    return os.path.join(config.UPLOAD_PATH, f"Upload-{uuid}.mp4")


def output_path(uuid):
    return os.path.join(config.OUTPUT_PATH, f"Output-{uuid}.mp4")


def position_path(uuid):
    return os.path.join(config.POSITION_PATH, f"{uuid}.json")


def start_workers():
    for name, worker in (("chopper", _chop_worker),
                         ("predictor", _predict_worker),
                         ("output-generator", _output_worker)):
        thread = threading.Thread(target=worker, name=name, daemon=True)
        thread.start()
        _workers[name] = thread


def worker_status():
    """Liveness and backlog of each stage, for /api/health.

    A dead thread is the failure worth catching here: the stages are daemon
    threads, so if one stops the process keeps serving uploads and every video
    handed to that stage silently stops advancing.
    """
    return {
        "chopper": _stage_status("chopper", _chop_queue),
        "predictor": _stage_status("predictor", _predict_queue),
        "output-generator": _stage_status("output-generator", _output_queue),
    }


def _stage_status(name, work_queue):
    thread = _workers.get(name)
    return {
        "alive": thread is not None and thread.is_alive(),
        "queued": work_queue.qsize(),
    }


def model_loaded():
    """False until the first video reaches the predict stage, which is normal."""
    return _model is not None


def _run_stage(name, work_queue, handler):
    while True:
        print(f"Waiting to {name}...", flush=True)
        item = work_queue.get()
        try:
            handler(item)
        except Exception as error:
            uuid = item[0] if isinstance(item, tuple) else item
            print(f"Failed to {name} {uuid}: {error}", flush=True)
        finally:
            work_queue.task_done()


def _chop_worker():
    _run_stage("chop", _chop_queue, _chop)


def _predict_worker():
    _run_stage("predict", _predict_queue, _predict)


def _output_worker():
    _run_stage("generate output", _output_queue, _generate_output)


def _chop(uuid):
    """Sample one frame every FRAME_TIME_INTERVAL seconds of the upload."""
    set_status(uuid, config.CHOPPING)
    print(f"Chopping {uuid}", flush=True)

    frame_dir = os.path.join(config.FRAME_PATH, uuid)
    os.makedirs(frame_dir, exist_ok=True)

    video = cv2.VideoCapture(upload_path(uuid))
    fps = video.get(cv2.CAP_PROP_FPS) or 30
    capture_interval = max(1, int(config.FRAME_TIME_INTERVAL * fps))

    frame_paths = []
    frame_number = 0
    n = 0
    while True:
        success, image = video.read()
        if not success:
            break
        if (n % capture_interval) == 0:
            frame_path = os.path.join(frame_dir, f"frame-{frame_number:06d}.jpg")
            cv2.imwrite(frame_path, image)
            frame_paths.append(frame_path)
            frame_number += 1
        n += 1
    video.release()

    set_status(uuid, config.CHOPPED)
    _predict_queue.put((uuid, frame_paths))


def _predict(item):
    """Track the climber's hips across the sampled frames."""
    uuid, frame_paths = item
    set_status(uuid, config.PREDICTING)
    print(f"Predicting for {uuid}", flush=True)

    global _model
    if _model is None:
        print("Loading model", flush=True)
        from ultralytics import YOLO
        _model = YOLO(config.MODEL_PATH)

    # prediction data structure: https://stackoverflow.com/questions/75121807/what-are-keypoints-in-yolov7-pose
    hip_positions = []
    for start in range(0, len(frame_paths), config.PREDICT_BATCH_SIZE):
        batch = frame_paths[start:start + config.PREDICT_BATCH_SIZE]
        for result in _model.predict(batch, verbose=False):
            if result.keypoints.conf is None:
                continue
            person = sorted(result.keypoints.xy, key=cmp_to_key(_sort_by_hip_height))[0]
            right_hip = person[11]
            left_hip = person[12]
            av_x = (right_hip[0] + left_hip[0]) // 2
            av_y = (right_hip[1] + left_hip[1]) // 2
            hip_positions.append((int(av_x), int(av_y)))

    with open(position_path(uuid), "w+") as position_file:
        json.dump(hip_positions, position_file)

    shutil.rmtree(os.path.join(config.FRAME_PATH, uuid), ignore_errors=True)

    set_status(uuid, config.PREDICTED)
    _output_queue.put(uuid)


def _sort_by_hip_height(person1, person2):
    # Smallest y is highest in the frame, i.e. the climber rather than the belayer.
    return person1[11][1] - person2[11][1]


def _generate_output(uuid):
    """Draw the tracked path onto every frame of the original video."""
    set_status(uuid, config.GENERATING_OUTPUT)
    print(f"Generating output for {uuid}", flush=True)

    with open(position_path(uuid), "r") as position_file:
        positions = [tuple(position) for position in json.load(position_file)]

    video = cv2.VideoCapture(upload_path(uuid))
    fps = video.get(cv2.CAP_PROP_FPS) or 30
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    encoder = _start_h264_encoder(output_path(uuid), width, height, fps)
    try:
        while True:
            success, frame = video.read()
            if not success:
                break
            for i in range(len(positions) - 1):
                cv2.line(frame, positions[i], positions[i + 1], (0, 0, 255), 2)
            encoder.stdin.write(frame.tobytes())
    finally:
        video.release()
        _finish_h264_encoder(encoder)

    os.remove(upload_path(uuid))
    # The position json is kept so the tracked path can be analysed afterwards.

    set_status(uuid, config.GENERATED_OUTPUT)


def _start_h264_encoder(destination, width, height, fps):
    """Pipe raw BGR frames into ffmpeg.

    The old output-generator wrote H.264 straight from OpenCV, which meant
    shipping openh264 shared libraries alongside a from-source OpenCV build.
    ffmpeg's libx264 does the same job with no extra binaries in the tree.
    """
    command = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "bgr24",
        "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        destination,
    ]
    return subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)


def _finish_h264_encoder(encoder):
    encoder.stdin.close()
    stderr = encoder.stderr.read().decode(errors="replace")
    encoder.stderr.close()
    if encoder.wait() != 0:
        raise RuntimeError(f"ffmpeg failed: {stderr.strip()}")
