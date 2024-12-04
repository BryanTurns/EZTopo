from flask import Flask, jsonify, request, make_response, send_file
import redis, hashlib, datetime, os, threading
from google.cloud import storage

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

print("Loading environment variables")
constants = {"BUCKET_NAME": "eztopo-bucket",
            "USER_UPLOAD_INITIATED": 2,
            "USER_UPLOAD_COMPLETE": 3,
            "USER_UPLOAD_PATH": "./data/input",
            "OUTPUT_PATH": "./data/output",
            "REDIS_HOST": "10.108.148.45",
            "REDIS_PORT": 6379}

print("Initiating storage")
storage_client = storage.Client.from_service_account_json("./key.json")
bucket = storage_client.bucket(constants["BUCKET_NAME"])

print("Initiating redis")
redisClient = redis.Redis(host=constants["REDIS_HOST"], port=constants["REDIS_PORT"])


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
    redisClient.rpush(username, uuid)

    fname = f"Upload-{uuid}"
    userFile.save(f"{constants['USER_UPLOAD_PATH']}/{fname}")
    # TODO: ADD COMPRESSION
    threading.Thread(target=upload_to_GCP, args=(uuid, fname)).start()
    
    return _corsify_actual_response(jsonify({"uuid": uuid})), 200


@app.route("/api/getOutputVideo", methods=["POST", "OPTIONS"])
def getOutput():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    try:
        requestData = request.get_json()
    except Exception as error:
        print("Invalid request format, expected json: ", error)
        return _corsify_actual_response(jsonify({"error": "Invalid request format, expected json: "})), 400
    try:
        uuid = requestData["uuid"]
    except Exception as error:
        print("No uuid in request: ", error)
        return _corsify_actual_response(jsonify({"error": "No uuid in request"}))
    
    outputFilename = f"Output-{uuid}.mp4"
    outputFilepath = f"{constants['OUTPUT_PATH']}/{outputFilename}"
    blob = bucket.blob(outputFilename)
    with open(outputFilepath, "wb") as outputFileobject:
        blob.download_to_file(outputFileobject)

    return _corsify_actual_response(send_file(outputFilepath, as_attachment=True))


@app.route("/api/checkStatus", methods=["POST", "OPTIONS"])
def check_status():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    
    try:
        requestData = request.get_json()
    except Exception as error:
        print("Invalid request format, expected json: ", error)
        return _corsify_actual_response(jsonify({"error": "Invalid request format, expected json: "})), 400
    try:
        uuid = requestData["uuid"]
    except Exception as error:
        print("No uuid in request: ", error)
        return _corsify_actual_response(jsonify({"error": "No uuid in request"}))
    
    status = redisClient.get(uuid)
    if status == None:
        status = -1

    return _corsify_actual_response(jsonify({"status": int(status)})), 200

@app.route("/api/test", methods=["GET", "OPTIONS"]) 
def helloworld():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
        
    return _corsify_actual_response(jsonify({"Result": "Hello, World"})), 200

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


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
    redisClient.rpush("chopQueue", uuid)

    print(f"{fname} upload complete")

    for filename in os.listdir(constants["USER_UPLOAD_PATH"]):
        os.remove(f"{constants['USER_UPLOAD_PATH']}/{filename}")

    return     

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