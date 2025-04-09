from client.grpc_client import GRPCClient
from orderservice.order_grpc import order_pb2, order_pb2_grpc
from client.grpc_product_client import ProductGRPCClient


class OrderGRPCClient:

    def retrieve(self, order_id):
        with GRPCClient("order") as channel:
            stub = order_pb2_grpc.OrderServiceStub(channel)
            request = order_pb2.OrderDetailRequest(id=order_id)

            response = stub.GetOrder(request)
            product_data = ProductGRPCClient().retrieve(product_id=response.product_id)
            return {
                "id": response.id,
                "product": product_data
            }


if __name__ == "__main__":
    called = OrderGRPCClient()
    print(called.retrieve(1))
