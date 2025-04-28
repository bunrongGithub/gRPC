import grpc
from account import account_pb2, account_pb2_grpc


def client():
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = account_pb2_grpc.UserControllerStub(channel=channel)
            response_stream = stub.List(account_pb2.UserListRequest())
            for i, user in enumerate(response_stream):
                print(f"User #{i+1}: {user}")

    except grpc.RpcError as e:
        print(f"ERROR: {e.code().name} - {e.details()}")
    except Exception as e:
        print(f"General error: {str(e)}")


if __name__ == "__main__":
    client()
