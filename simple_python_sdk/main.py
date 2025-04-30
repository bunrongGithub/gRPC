
from core.connection.grpc_connection import GrpcConnection


def main():
    GrpcConnection(grpc_server_add="localhost:50052")
if __name__ == "__main__":
    main()