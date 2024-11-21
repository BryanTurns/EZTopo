from flask import Flask
import grpc, redis
from eztopo_utils.grpc import chopper_pb2, chopper_pb2_grpc, checkConnection_pb2, checkConnection_pb2_grpc
import eztopo_utils.constants as constants 
from minio import Minio

app = Flask(__name__)

redisClient = redis.Redis(host=constants.REDIS_HOST, port=constants.REDIS_PORT)

minioHost = constants.MINIO_HOST
minioUser = constants.MINIO_USER
minioPasswd = constants.MINIO_PASSWORD
minioClient = Minio(minioHost,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

# Setup grpc for chopper
chopperChannel = grpc.insecure_channel(f"{constants.CHOPPER_HOST}:{constants.CHOPPER_PORT}")
chopperStub = chopper_pb2_grpc.chopperStub(chopperChannel)
chopperCheckConnectionStub = checkConnection_pb2_grpc.checkConnectionStub(chopperChannel)

@app.route("/api/uploadVideo")
def chop_video():
    return "<p>Uploading</p>"

@app.route("/api/checkStatus")
def check_status():
    return "Checking status"

@app.route("/checkChopper")
def hello_world():
    response = chopperCheckConnectionStub.CheckConnection(checkConnection_pb2.checkMessage(message="Hello, World"))
    return response.message


