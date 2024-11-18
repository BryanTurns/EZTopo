FROM python:3.8

RUN mkdir /app && \
    cd /app && \
    mkdir data && \
    pip3 install --upgrade flask 

WORKDIR /app

COPY frame-chopper.py /app/frame-chopper.py

CMD [ "python3", "frame-chopper.py"]