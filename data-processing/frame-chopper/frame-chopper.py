import cv2, os, grpc, redis
from concurrent import futures
from eztopo_utils.grpc import chopper_pb2, chopper_pb2_grpc, checkConnection_pb2, checkConnection_pb2_grpc
from minio import Minio
import eztopo_utils.constants as constants


redisClient = redis.Redis(host=constants.REDIS_HOST, port=constants.REDIS_PORT)


minioHost = constants.MINIO_HOST
minioUser = constants.MINIO_USER
minioPasswd = constants.MINIO_PASSWORD
minioClient = Minio(minioHost,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)


class ChopperServicer(chopper_pb2_grpc.chopperServicer):
    def Chop(self, request, context):
        videoHash = request.hash
        originalStatus = redisClient.get(videoHash)
        # Check if the video is ready to chop
        # if originalStatus != SOME_CONSTANT:
        #     err
        video = minioClient.get_object("eztopo-bucket", f"original-{videoHash}.mp4", "./data/input.mp4")
        videoObject = cv2.VideoCapture("./input.mp4")

        fps = int(videoObject.get(cv2.CAP_PROP_FPS))
        # Every frameCaptureInteval, save a frame
        frameCaptureInterval = int(constants.FRAME_TIME_INTERVAL * fps)
        # Number of frames read
        n = 0
        success = True
        while success:
            # Read a frame
            success, image = videoObject.read()
            # Every frameCaptureInterval, save the frame
            if (n % frameCaptureInterval) == 0:
                frameNumber = n // frameCaptureInterval
                savePath = f"./data/frame-{frameNumber}-{videoHash}.jpg"
                # Consider changing img quality in params
                cv2.imwrite(savePath, image)
            n = n + 1
        
        # Clear files from data for next call
        dataFiles = os.listdir("./data")
        for file in dataFiles:
            os.remove(f"./data/{file}")

        return chopper_pb2.chopReply(err=0)
        

class checkConnectionServicer(checkConnection_pb2_grpc.checkConnectionServicer):
    def CheckConnection(self, request, context):
        print(request.message)
        return checkConnection_pb2.checkReply(message="Hello from chopper")
        

def grpc_main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chopper_pb2_grpc.add_chopperServicer_to_server(ChopperServicer(), server)
    checkConnection_pb2_grpc.add_checkConnectionServicer_to_server(checkConnectionServicer(), server)
    server.add_insecure_port(f'[::]:{constants.CHOPPER_PORT}')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    grpc_main()

