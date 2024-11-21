# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

# import chopper_pb2 as chopper__pb2
from . import chopper_pb2 as chopper__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in chopper_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class chopperStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Chop = channel.unary_unary(
                '/chopper.chopper/Chop',
                request_serializer=chopper__pb2.chopMessage.SerializeToString,
                response_deserializer=chopper__pb2.chopReply.FromString,
                _registered_method=True)


class chopperServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Chop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_chopperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Chop': grpc.unary_unary_rpc_method_handler(
                    servicer.Chop,
                    request_deserializer=chopper__pb2.chopMessage.FromString,
                    response_serializer=chopper__pb2.chopReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chopper.chopper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('chopper.chopper', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class chopper(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Chop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/chopper.chopper/Chop',
            chopper__pb2.chopMessage.SerializeToString,
            chopper__pb2.chopReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
