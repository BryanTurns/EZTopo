FROM python:3.8

RUN mkdir /data && \
    mkdir /data/input && \
    mkdir /data/output 

ENV FLASK_PORT=5000
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

RUN pip3 install flask google-cloud-storage redis 

COPY key.json key.json
COPY rest-server.py app.py

CMD [ "flask", "run", "--host=0.0.0.0"]