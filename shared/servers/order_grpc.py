import grpc
import os

import orderservice.order_grpc.order_pb2_grpc as pb2_grpc
from concurrent import futures
from ..services.order_service import OrderService


GRPC_ORDER_HOST = os.getenv("GRPC_ORDER_HOST")


def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port(GRPC_ORDER_HOST)
    server.start()
    print("Server started on port ", GRPC_ORDER_HOST)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
