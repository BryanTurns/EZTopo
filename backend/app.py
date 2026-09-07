import datetime
import hashlib
import os
import shutil

import config
import pipeline
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_UPLOAD_BYTES

for path in config.WORKING_PATHS:
    os.makedirs(path, exist_ok=True)

pipeline.start_workers()


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


@app.route("/api/uploadVideo", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "Request did not include file"}), 400
    username = request.form.get("username")
    if not username:
        return jsonify({"error": "Request did not include username"}), 400

    # Create a uuid based off time and username
    uuid_pre_hash = str(datetime.datetime.now()) + username
    uuid = hashlib.sha256(uuid_pre_hash.encode()).hexdigest()

    pipeline.set_status(uuid, config.USER_UPLOAD_INITIATED)
    request.files["file"].save(pipeline.upload_path(uuid))
    pipeline.set_status(uuid, config.USER_UPLOAD_COMPLETE)
    pipeline.submit(uuid)

    return jsonify({"uuid": uuid}), 200


@app.route("/api/checkStatus", methods=["POST"])
def check_status():
    uuid = _uuid_from_request()
    if uuid is None:
        return jsonify({"error": "No uuid in request"}), 400

    return jsonify({"status": pipeline.get_status(uuid)}), 200


@app.route("/api/getOutputVideo", methods=["POST"])
def get_output_video():
    uuid = _uuid_from_request()
    if uuid is None:
        return jsonify({"error": "No uuid in request"}), 400

    output = pipeline.output_path(uuid)
    if not os.path.exists(output):
        return jsonify({"error": "No output video for that uuid"}), 404

    return send_file(output, as_attachment=True)


@app.route("/api/health", methods=["GET"])
def health():
    """Report whether this instance can actually process a video.

    200 when every dependency the pipeline needs is present and all three
    stages are running, 503 otherwise, so a container orchestrator or load
    balancer can pull a broken instance out of rotation.
    """
    workers = pipeline.worker_status()
    checks = {
        "workers": workers,
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "model_file": os.path.exists(config.MODEL_PATH),
        "data_dirs": all(os.path.isdir(path) and os.access(path, os.W_OK)
                         for path in config.WORKING_PATHS),
        # Informational: the model is loaded lazily by the first prediction, so
        # False here is normal on a freshly started instance and not a failure.
        "model_loaded": pipeline.model_loaded(),
    }

    healthy = (
        all(stage["alive"] for stage in workers.values())
        and checks["ffmpeg"]
        and checks["model_file"]
        and checks["data_dirs"]
    )

    body = {"status": "ok" if healthy else "degraded", "checks": checks}
    return jsonify(body), 200 if healthy else 503


@app.route("/api/test", methods=["GET"])
def helloworld():
    return jsonify({"Result": "Hello, World"}), 200


def _uuid_from_request():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return None
    return body.get("uuid")
