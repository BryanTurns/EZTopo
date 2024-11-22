from flask import Flask, jsonify
import grpc, redis
from eztopo_utils.grpc import chopper_pb2, chopper_pb2_grpc, checkConnection_pb2, checkConnection_pb2_grpc
import eztopo_utils.constants as constants 
from minio import Minio
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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


# @cross_origin
@app.route("/api/uploadVideo", methods=["POST"])
def chop_video():
    return jsonify({"status": "success"})

@app.route("/api/uploadChunk", methods=["POST"])

@app.route("/api/checkStatus")
def check_status():
    return "Checking status"

@app.route("/api/checkChopper")
def hello_world():
    response = chopperCheckConnectionStub.CheckConnection(checkConnection_pb2.checkMessage(message="Hello, World"))
    return response.message

@app.route("/api")
def home():
    return "Hello, World"


