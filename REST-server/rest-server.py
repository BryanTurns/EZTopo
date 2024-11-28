from flask import Flask, jsonify, request, make_response
import redis, hashlib, datetime, os, threading
from google.cloud import storage
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

load_dotenv("../.env")
constants = {"PROJECT_NAME": os.getenv("PROJECT_NAME"), 
            "BUCKET_NAME": os.getenv("BUCKET_NAME"),
            "USER_UPLOAD_INITIATED": os.getenv("USER_UPLOAD_INITIATED"),
            "USER_UPLOAD_COMPLETE": os.getenv("USER_UPLOAD_COMPLETE"),
            "USER_UPLOAD_PATH": os.getenv("USER_UPLOAD_PATH")}

storage_client = storage.Client()
bucket = storage_client.bucket(constants["BUCKET_NAME"])

redisClient = redis.Redis(host="localhost", port=6379)


@app.route("/api/uploadVideo", methods=["POST", "OPTIONS"])
def start_upload():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    try:
        userFile = request.files["file"]
    except Exception as error:
        print("No file sent: ", error)
        return _corsify_actual_response(jsonify({"error": "Request did not include file"})), 400
    try:
        username = request.form.get("username")
    except Exception as error:
        print("No username sent ", error)
        return _corsify_actual_response(jsonify({"error": "Request did not include username"})), 400
    
    # Create a uuid based off time and username
    currentTime = str(datetime.datetime.now())
    uuidPreHash = currentTime + username
    uuid = str(hashlib.sha256(uuidPreHash.encode()).hexdigest())

    redisClient.set(uuid, constants["USER_UPLOAD_INITIATED"])

    fname = f"{username}-Upload-{uuid}"
    userFile.save(f"{constants['USER_UPLOAD_PATH']}/{fname}")
    # TODO: ADD COMPRESSION
    threading.Thread(target=upload_to_GCP, args=(uuid, fname)).start()
    
    return _corsify_actual_response(jsonify({"uuid": uuid})), 200


def upload_to_GCP(uuid, fname):
    try:
        blob = bucket.blob(fname)
    except Exception as error:
        print("Could not create blob: ", error)
    try: 
        blob.upload_from_filename(f"{constants['USER_UPLOAD_PATH']}/{fname}")
    except Exception as error:
        print("Could not upload blob: ", error)

    redisClient.set(uuid, constants["USER_UPLOAD_COMPLETE"])
    redisClient.lpush("chopQueue", uuid)

    print(f"{fname} upload complete")

    for filename in os.listdir(constants["USER_UPLOAD_PATH"]):
        os.remove(f"{constants['USER_UPLOAD_PATH']}/{filename}")

    return     


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    return response


# @app.route("/api/startUpload", methods=["POST", "OPTIONS"])
# def start_upload():
#     if request.method == "OPTIONS":
#         return _build_cors_preflight_response()
    
#     try:
#         requestData = request.get_json()
#     except Exception as e:
#         print("Failed to parse JSON: ", e)
#         return _corsify_actual_response(jsonify({"error": "Failed to parse JSON"})), 400
    

#     try:
#         username = requestData["username"]
#     except Exception as e:
#         print("Request did not include username: ", e) 
#         return _corsify_actual_response(jsonify({"error": "Request did not include username"})), 400
    
#     # Create a uuid based off time and username
#     currentTime = str(datetime.datetime.now())
#     uuidPreHash = currentTime + username
#     uuid = str(hashlib.sha256(uuidPreHash.encode()).hexdigest())

#     redisClient.set(uuid, constants.INITIAL_UPLOAD)

#     return _corsify_actual_response(jsonify({"uuid": uuid})), 200
    
# @app.route("/api/uploadChunk", methods=["POST", "OPTIONS"])
# def upload_chunk():
#     # Handle CORS
#     if request.method == "OPTIONS":
#         return _build_cors_preflight_response()
    
#     try:
#         chunk = request.files["file"]
#     except Exception as error:
#         print("No file sent: ", error)
#         return _corsify_actual_response(jsonify({"error": "Request did not include file"})), 400
    
#     chunk.seek(0)

#     try:
#         chunkNumber = request.form.get("chunkNumber")
#     except Exception as error:
#         print("No chunkNumber sent ", error)
#         return _corsify_actual_response(jsonify({"error": "Request did not include chunkNumber"})), 400
    
#     try:
#         uuid = request.form.get("uuid")
#     except Exception as error:
#         print("No uuid sent: ", error)
#         return _corsify_actual_response(jsonify({"error": "Request did not include uuid"}))
    
#     print(f"Recieved chunk {chunkNumber} of {chunk.filename} ({uuid})")
#     # TODO: Make it work with minio/redis
#     chunkName = f"{uuid}-chunk-{chunkNumber}"
    
#     blob = bucket.blob(chunkName)
#     blob.upload_from_file(chunk)
    
#     return _corsify_actual_response(jsonify({"data": "skdjdsklfj"})), 200