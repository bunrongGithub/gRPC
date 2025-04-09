import grpc
import os

import productservice.product_grpc.product_pb2 as pb2
import productservice.product_grpc.product_pb2_grpc as pb2_grpc
from concurrent import futures
from .services.product_service import ProductService


GRPC_PRODUCT_HOST = os.getenv("GRPC_PRODUCT_HOST")


def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port(GRPC_PRODUCT_HOST)
    server.start()
    print("Server started on port ", GRPC_PRODUCT_HOST)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
