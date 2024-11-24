from flask import Flask, jsonify, request, make_response
import grpc, redis, sys
from eztopo_utils.grpc import chopper_pb2, chopper_pb2_grpc, checkConnection_pb2, checkConnection_pb2_grpc
import eztopo_utils.constants as constants 
from eztopo_utils.fingerprint import generateFingerprintFromObject
from minio import Minio
# from flask_cors import CORS, cross_origin


app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


redisClient = redis.Redis(host=constants.REDIS_HOST, port=constants.REDIS_PORT)

minioHost = constants.MINIO_HOST
minioUser = constants.MINIO_USER
minioPasswd = constants.MINIO_PASSWORD
minioClient = Minio(minioHost,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)

chopperChannel = grpc.insecure_channel(f"{constants.CHOPPER_HOST}:{constants.CHOPPER_PORT}")
chopperStub = chopper_pb2_grpc.chopperStub(chopperChannel)
chopperCheckConnectionStub = checkConnection_pb2_grpc.checkConnectionStub(chopperChannel)

currentUploads = []

# @cross_origin
@app.route("/api/uploadVideo", methods=["POST"])
def chop_video():
    return jsonify({"status": "success"})

# @app.route("/api/startUpload", methods=["POST"])
# def start_upload():


@app.route("/api/uploadChunk", methods=["POST", "OPTIONS"])
def upload_chunk():
    # Handle CORS
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    try:
        requestData = request.get_json()
        videoChunk = requestData['chunk']
    except Exception as error:
        print("Invalid format: ", error)
        return _corsify_actual_response(jsonify({}), 400)

    chunkHash = ""

    response = {"hash": chunkHash}
    print(response)
    return _corsify_actual_response(jsonify(response), 200)


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


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response, status):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status