FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    EZTOPO_DATA_DIR=/data \
    YOLO_CONFIG_DIR=/tmp/ultralytics

# ffmpeg encodes the browser-playable H.264 output; libgl/libglib are OpenCV's
# runtime dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# CPU-only torch, which is a fraction of the size of the default CUDA wheels.
RUN pip3 install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
        torch torchvision

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY models/ ./models/
COPY config.py pipeline.py app.py ./

RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/api/health').read()"

# One worker so the pipeline threads and their in-memory job state are shared by
# every request; threads keep uploads and polling responsive while it works.
CMD ["gunicorn", "--workers", "1", "--threads", "8", "--timeout", "0", \
     "--bind", "0.0.0.0:5000", "app:app"]
