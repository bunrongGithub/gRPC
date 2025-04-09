import grpc
from orderservice.order_grpc import order_pb2_grpc, order_pb2
from orderservice.models import Order


class OrderService(order_pb2_grpc.OrderServiceServicer):
    model = Order.objects.all()

    def get_query_set(self):
        return self.model

    def GetOrder(self, request, context):
        try:
            order = self.get_query_set().get(id=request.id)
            return order_pb2.OrderResponse(
                id=order.id,
                user_id=order.user_id,
                product_id=order.product_id,
                message="",
            )
        except grpc.RpcError as e:
            raise e
