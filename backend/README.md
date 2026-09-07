# EZTopo backend

One image, one process. `app.py` serves the API, `pipeline.py` runs the three
processing stages, `config.py` holds the paths, tunables and status codes.

This replaces what used to be four services (rest-server, video-chopper,
position-predictor, output-generator) coordinating through Redis queues and a
Google Cloud Storage bucket. The queues are now `queue.Queue`, the bucket is now
the `/data` directory, and each stage is a worker thread rather than a pod. The
stages still run concurrently, so one video can be having its path drawn while
the next is still being chopped.

## Routes

- `POST /api/uploadVideo` — multipart `file` and `username`. Saves the video,
  starts processing, returns `{"uuid": ...}`.
- `POST /api/checkStatus` — `{"uuid": ...}` in, `{"status": <int>}` out.
- `POST /api/getOutputVideo` — `{"uuid": ...}` in, the finished mp4 out. 404 until
  the status reaches 9.
- `GET /api/test` — health check.

## Status codes

The frontend maps these in `translateStatus()`, so they must stay stable.

| Code | Meaning |
| ---- | ------- |
| -1 | Unknown UUID |
| 2 | Upload initiated |
| 3 | Upload complete |
| 4 | Chopping video into frames |
| 5 | Chopped |
| 6 | Running frames through the pose model |
| 7 | Positions predicted |
| 8 | Drawing the path onto the video |
| 9 | Done |

Statuses live in memory, so they are lost if the container restarts.

## Environment variables

| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `EZTOPO_DATA_DIR` | `/data` | Where uploads, frames, position JSON and outputs go |
| `EZTOPO_MODEL_PATH` | `./models/yolo11s-pose.pt` | Pose model weights |
| `EZTOPO_FRAME_INTERVAL` | `1` | Seconds of video between sampled frames |
| `EZTOPO_PREDICT_BATCH` | `16` | Frames given to the model at a time |

## Notes

- Gunicorn runs a **single** worker on purpose. Job status and the queues are
  in-process, so a second worker would not see them. Threads keep uploads and
  status polling responsive while the pipeline works.
- Output is encoded by piping raw frames into `ffmpeg`'s libx264. The old
  output-generator got H.264 out of OpenCV directly, which meant a from-source
  OpenCV build plus checked-in openh264 `.so`/`.dll` files; those are gone.
- Uploads, frames and the source video are deleted as they are consumed. The
  position JSON is kept under `positions/` so a traced path can be analysed
  afterwards.
