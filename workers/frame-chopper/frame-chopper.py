import cv2, os, grpc, redis
from concurrent import futures
from eztopo_utils.chopper import chopper_pb2, chopper_pb2_grpc
from minio import Minio
from eztopo_utils.constants import FRAME_TIME_INTERVAL


# Number of seconds between saved frames


# IP is static (refer to /message-queue/redis-service.yaml)
redisClient = redis.Redis(host="10.108.148.45", port=6379)


minioHost = os.getenv("MINIO_HOST") or "minio-proj.minio-ns.svc.cluster.local:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioClient = Minio(minioHost,
               secure=False,
               access_key=minioUser,
               secret_key=minioPasswd)


class ChopperServicer(chopper_pb2_grpc.chopperServicer):
    def Chop(self, request, context):
        dataFiles = os.listdir("./data")
        for file in dataFiles:
            os.remove(f"./data/{file}")

        videoHash = request.hash
        originalStatus = redisClient.get(videoHash)
        # Check if the video is ready to chop
        # if originalStatus != SOME_CONSTANT:
        #     err
        video = minioClient.get_object("eztopo-bucket", f"original-{videoHash}.mp4", "./data/input.mp4")
        videoObject = cv2.VideoCapture("./input.mp4")

        fps = int(videoObject.get(cv2.CAP_PROP_FPS))
        # Every frameCaptureInteval, save a frame
        frameCaptureInterval = int(FRAME_TIME_INTERVAL * fps)
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
        

def grpc_main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chopper_pb2_grpc.add_chopperServicer_to_server(ChopperServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    grpc_main()

