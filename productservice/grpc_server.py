import os 
import sys
import grpc
# from product_pb2_grpc import add_ProductServiceServicer_to_server

from concurrent import futures
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","microservices.settings")
import django
django.setup()
from productservice.product_grpc import product_pb2_grpc as product__pb2_grpc
# import productservice.product_grpc.product_pb2_grpc as product__pb2_grpc
from services import grpc_service
# import product_grpc.product_pb2
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product__pb2_grpc.add_ProductServiceServicer_to_server(grpc_service.ProductService(),server=server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server running on port localhost:50051...")
    server.start()
    server.wait_for_termination()


if __name__ =="__main__":
    serve()