FROM python:3.8

RUN mkdir /app && \
    mkdir /app/data && \
    cd /app && \
    pip3 install --upgrade opencv-python-headless grpcio redis minio eztopo-utils protobuf

WORKDIR /app

COPY video-chopper.py /app/video-chopper.py
COPY startup.sh /app/startup.sh

CMD [ "/bin/bash", "-c", "./startup.sh"]