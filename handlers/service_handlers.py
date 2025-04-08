from productservice.product_grpc import product_pb2_grpc
from productservice.service import ProductService
from orderservice.order_grpc import order_pb2_grpc


def grpc_handlers(server):
    print("GRPC Handler Service start:: ")
    product_pb2_grpc.add_ProductServiceServicer_to_server(
        servicer=ProductService.as_servicer(), server=server
    )
    order_pb2_grpc.add_OrderServiceServicer_to_server(
        servicer=ProductService.as_servicer(), server=server
    )

if __name__ == "__main__":
    grpc_handlers("0.0.0.0:50051")