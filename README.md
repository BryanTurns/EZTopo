# EZTopo

Project Structure:

1. The frontend is under the web-server directory. Refer to ./web-server/README.md for more information. The frontend is only responsible for getting, sending, and displaying user data.
2. The backend REST server is under the rest-server directory. Refer to ./rest-server for more information. The REST service is responsible for storing the raw video and making calls to the frame-chopper service.
3. The conversion of video to topology is under the data-processing directory. Refer to ./data-processing for more information.
4. The message queue is under message-queue. Refer to ./message-queue/README.md for more information. It is currently implemented with Redis.
5. Object storage is done under ./object-store. Refer to ./object-store/README.md for more information. It is currently implemented with Minio.
6. Networking (ingress) is done under ./networking. Refer to ./networking/README.md for more information. It is currently implemented with ngix.
7. GRPC and other utilties like constants exist under ./eztopo_utils.

Running the Code:

1. Install docker and enable kubernetes
2. Run ./deploy-local.sh
3. The frontend will now be accessible at localhost:80

Starting the cluster:

1. Run deploy-local.sh

If you make changes to eztopo_utils:

1. Navigate to eztopo directory
2. Update setup.py version
3. python3 setup.py sdist
4. python3 setup.py bdist_wheel
5. python3 -m twine upload dist/\*

If you change any proto:

1. naviage to /eztopo_utils/grpc
2. python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./chopper.proto
3. change "import chopper\_\_pb2 as chopper\_\_pb2" to "from . import chopper_pb2 as chopper\_\_pb2"
   WHEN COMPILING
