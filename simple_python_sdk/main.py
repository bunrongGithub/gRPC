import asyncio
from simple_python_sdk.core.api import GrpcSDK
from simple_python_sdk.core.events.store import RedisEventStore

async def handle_order_created(event):
    print(f"New order created! ID: {event['order_id']}")
    print(f"Details: {event}")

async def main():
    sdk = GrpcSDK(grpc_server_add="localhost:50052",redis_url="redis://localhost:6379/0")
    # Register event handler
    sdk.register_event_handler("order_created", handle_order_created)
    try:
        # Create an order
        new_order = await sdk.order.create_order(
            user_id=123,
            product_id=456
        )
        # Retrieve an order
        order_details = await sdk.order.get_order(
            order_id=new_order['id']
        )
        print(f"Order details: {order_details}")
        
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())