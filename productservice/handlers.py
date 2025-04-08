from productservice.service import ProductService
from product_grpc import product_pb2_grpc


def product_grpc_handler(server):
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        servicer=ProductService.as_servicer(), server=server
    )
