FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk2.0-dev \
    pkg-config \
    python3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    gfortran \
    libatlas-base-dev \
    x264 \
    libopencv-dev \
    ffmpeg
RUN pip3 install redis google-cloud-storage
RUN pip3 install --no-binary opencv-python opencv-python
RUN mkdir /data && \
    mkdir /data/input && \
    mkdir /data/output

COPY ./output-generator.py output-generator.py



CMD [ "python3", "output-generator.py"]