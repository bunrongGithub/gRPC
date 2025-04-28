from account import services
from account import account_pb2_grpc


def account_grpc_app_handler(server):
    account_pb2_grpc.add_UserControllerServicer_to_server(
        servicer=services.UserService, server=server
    )
