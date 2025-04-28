# simple_python_sdk/core/clients/order_client.py
from simple_python_sdk import order_pb2, order_pb2_grpc
from ..connection.manager import ConnectionManager
from ..events.dispatcher import EventDispatcher


class OrderClient:
    def __init__(
        self, 
        connection_manager: ConnectionManager, 
        event_dispatcher: EventDispatcher
    ):
        self.conn = connection_manager
        self.dispatcher = event_dispatcher

    async def get_order(self, order_id: int):
        """Get order details"""
        try:
            # Dispatch event before call
            await self.dispatcher.dispatch(
                "order_retrieve_start",
                {"order_id": order_id}
            )
            
            # Get the stub
            get_stub = stub = await self.conn.get_stub(
                "order",
                order_pb2_grpc.OrderServiceStub
            )

            # Make the gRPC call
            request = order_pb2.OrderDetailRequest(id=order_id)
            response = await stub.GetOrder(request)
            
            # Dispatch success event
            await self.dispatcher.dispatch(
                "order_retrieved",
                {
                    "order_id": order_id,
                    "details": {
                        "user_id": response.user_id,
                        "product_id": response.product_id,
                        "message": response.message
                    }
                }
            )
            
            return {
                "id": response.id,
                "user_id": response.user_id,
                "product_id": response.product_id,
                "message": response.message
            }
            
        except Exception as e:
            await self.dispatcher.dispatch(
                "order_retrieve_failed",
                {
                    "order_id": order_id,
                    "error": str(e)
                }
            )
            raise

    async def create_order(self, user_id: int, product_id: int):
        """Create new order"""
        try:
            await self.dispatcher.dispatch(
                "order_create_start",
                {"user_id": user_id, "product_id": product_id}
            )
            
            stub = await self.conn.get_stub(
                "order",
                order_pb2_grpc.OrderServiceStub
            )
            
            request = order_pb2.OrderRequest(
                user_id=user_id,
                product_id=product_id
            )
            response = await stub.CreateOrder(request)
            
            await self.dispatcher.dispatch(
                "order_created",
                {
                    "order_id": response.id,
                    "user_id": response.user_id,
                    "product_id": response.product_id
                }
            )
            
            return {
                "id": response.id,
                "message": response.message
            }
            
        except Exception as e:
            await self.dispatcher.dispatch(
                "order_create_failed",
                {
                    "user_id": user_id,
                    "product_id": product_id,
                    "error": str(e)
                }
            )
            raise