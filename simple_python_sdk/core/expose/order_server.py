from concurrent import futures
import grpc
import simple_python_sdk.order_pb2 as order_pb2
import simple_python_sdk.order_pb2_grpc as order_pb2_grpc

# In-memory "fake database"
ORDERS = {}
ORDER_ID_COUNTER = 1

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        global ORDER_ID_COUNTER
        order_id = ORDER_ID_COUNTER
        ORDER_ID_COUNTER += 1

        ORDERS[order_id] = {
            "user_id": request.user_id,
            "product_id": request.product_id
        }

        return order_pb2.OrderResponse(
            id=order_id,
            user_id=request.user_id,
            product_id=request.product_id,
            message="Order created successfully"
        )

    def GetOrder(self, request, context):
        print(f"Received GetOrder: id={request.id}")
        order = ORDERS.get(request.id)
        if not order:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Order {request.id} not found")
            return order_pb2.OrderResponse()

        return order_pb2.OrderResponse(
            id=request.id,
            user_id=order["user_id"],
            product_id=order["product_id"],
            message="Order fetched successfully"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port("[::]:50052")  # localhost:50052
    server.start()
    print("gRPC server started on localhost:50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
