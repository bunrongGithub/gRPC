import grpc
from authservice import auth_pb2
from authservice import auth_pb2_grpc as auth_grpc

def run_client():
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = auth_grpc.AuthServiceStub(channel)
            
            # Test Login - CORRECT way
            login_request = auth_pb2.LoginRequest(
                username="testuser",
                password="testpass"
            )
            login_response = stub.Login(login_request)
            print("Login Response:", login_response)
            
            # Test GetUser - NEW method
            user_request = auth_pb2.UserRequest(id=1)
            user_response = stub.GetUser(user_request)
            print("User Response:", user_response)
            
    except grpc.RpcError as e:
        print(f"gRPC error occurred: {e.code().name}: {e.details()}")
        if e.code() == grpc.StatusCode.UNIMPLEMENTED:
            print("Make sure the server has implemented this method")

if __name__ == "__main__":
    run_client()