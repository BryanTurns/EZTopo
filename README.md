# EZTopo

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
