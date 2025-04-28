
from simple_python_sdk.core.clients.example import OrderClient
from simple_python_sdk.core.connection.manager import ConnectionManager
from simple_python_sdk.core.events.dispatcher import EventDispatcher


class GrpcSDK:
    def __init__(self, grpc_server_add: str, redis_url: str):
        self.event_dispatcher = EventDispatcher(redis_url)
        self.conn_manager = ConnectionManager(grpc_server_add, self.event_dispatcher)
        
        # Initialize order client
        self.order = OrderClient(self.conn_manager, self.event_dispatcher)

    def register_event_handler(self, event_type: str, handler:callable):
        """Public method to register event handlers"""
        self.event_dispatcher.register_handler(event_type, handler)
    
    async def __aenter__(self):
        await self.conn_manager.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn_manager.close()