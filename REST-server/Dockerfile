FROM python:3.8

RUN mkdir /app && \
    cd /app && \
    mkdir data && \
    pip3 install --upgrade flask 

WORKDIR /app

ENV FLASK_PORT=5000

EXPOSE 5000

COPY rest-server.py /app/app.py

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]