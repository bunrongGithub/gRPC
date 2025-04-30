from simple_python_sdk.core.api import GrpcConnection
def main():
    # Example Connection
    GrpcConnection(grpc_server_add="localhost:50052")
if __name__ == "__main__":
    main()