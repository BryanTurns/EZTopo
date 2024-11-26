from flask import Flask, jsonify, request, make_response
import grpc, redis, sys, hashlib, datetime
import eztopo_utils.constants as constants 
from minio import Minio
# from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

LOCAL = True

if not LOCAL:
    redisClient = redis.Redis(host=constants.REDIS_HOST, port=constants.REDIS_PORT)

    minioHost = constants.MINIO_HOST
    minioUser = constants.MINIO_USER
    minioPasswd = constants.MINIO_PASSWORD
    minioClient = Minio(minioHost,
                secure=False,
                access_key=minioUser,
                secret_key=minioPasswd)
else:
    redisClient = redis.Redis(host="localhost", port=6379)

    minioHost = "localhost:9000"
    minioUser = constants.MINIO_USER
    minioPasswd = constants.MINIO_PASSWORD
    minioClient = Minio(minioHost,
                secure=False,
                access_key=minioUser,
                secret_key=minioPasswd)

uploadCounter = 0

# @cross_origin
@app.route("/api/uploadVideo", methods=["POST"])
def chop_video():
    return jsonify({"status": "success"})

@app.route("/api/startUpload", methods=["POST", "OPTIONS"])
def start_upload():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    try:
        requestData = request.get_json()
    except Exception as e:
        print("Failed to parse JSON: ", e)
        return _corsify_actual_response(jsonify({"error": "Failed to parse JSON"})), 400
    

    try:
        username = requestData["username"]
    except Exception as e:
        print("Request did not include username: ", e) 
        return _corsify_actual_response(jsonify({"error": "Request did not include username"})), 400
    
    currentTime = str(datetime.datetime.now())
    uuidPreHash = currentTime + username
    uuid = str(hashlib.sha256(uuidPreHash.encode()).hexdigest())

    redisClient.set(uuid, constants.INITIAL_UPLOAD)

    return _corsify_actual_response(jsonify({"uuid": uuid})), 200
    

    

@app.route("/api/uploadChunk", methods=["POST", "OPTIONS"])
def upload_chunk():
    # Handle CORS
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    try:
        chunk = request.files["file"]
    except Exception as error:
        print("No file sent: ", error)
        return _corsify_actual_response(jsonify({"error": "Request did not include file"})), 400
    
    try:
        chunkNumber = request.form.get("chunkNumber")
    except Exception as error:
        print("No chunkNumber sent ", error)
        return _corsify_actual_response(jsonify({"error": "Request did not include chunkNumber"})), 400
    
    try:
        uuid = request.form.get("uuid")
    except Exception as error:
        print("No uuid sent: ", error)
        return _corsify_actual_response(jsonify({"error": "Request did not include uuid"}))
    
    

    print(f"Recieved chunk {chunkNumber} of {chunk.filename} ({uuid})")

    # TODO: Make it work with minio/redis
    chunkName = f"{uuid}-chunk-{chunkNumber}"
    # res = minioClient.put_object("eztopo-bucket", chunkName, chunk)

    # print(res)
    
    return _corsify_actual_response(jsonify({"data": "skdjdsklfj"})), 200



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
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    return response