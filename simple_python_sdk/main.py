from simple_python_sdk.core.api import GrpcSDKConnection
def main():
    # Example Connection
    GrpcSDKConnection(grpc_server_add="localhost:50052")
if __name__ == "__main__":
    main()