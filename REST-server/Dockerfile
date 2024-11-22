FROM python:3.8

RUN mkdir /app && \
    cd /app && \
    mkdir data && \
    pip3 install --upgrade flask grpcio redis minio protobuf flask-cors

WORKDIR /app

ENV FLASK_PORT=5000
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

COPY rest-server.py /app/app.py
COPY startup.sh /app/startup.sh

CMD [ "/bin/bash", "-c", "./startup.sh"]