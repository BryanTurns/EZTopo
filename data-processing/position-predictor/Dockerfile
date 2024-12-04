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
    libatlas-base-dev 
RUN pip3 install opencv-python redis google-cloud-storage 
RUN pip3 install torch torch-vision ultralytics
RUN mkdir /data && \
    mkdir /data/input && \
    mkdir /data/output

COPY ./key.json key.json

COPY ./position-predictor.py position-predictor.py

CMD [ "python3", "position-predictor.py"]