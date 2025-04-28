from ast import Dict
import asyncio
from typing import Any

import grpc

from simple_python_sdk.core.events.dispatcher import EventDispatcher


class ConnectionManager:
    def __init__(
        self,
        address: str,
        event_dispatcher: EventDispatcher,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        self.address = address
        self.event_dispatcher = event_dispatcher
        self.max_retries = max_retries
        self.timeout = timeout
        self._channel = None
        self._stubs: Dict[str, Any] = {}

    async def connect(self):
        """Establish gRPC connection with retry logic"""
        if self._channel is not None:
            print("Skip")
            return
        """Do Connection"""
        retry_count = 0
        last_error = None
        while retry_count < self.max_retries:
            try:
                self._channel = grpc.aio.insecure_channel(
                    target=self.address,
                    # credentials=grpc.ssl_channel_credentials(
                    #     root_certificates=None,
                    #     private_key=None,
                    #     certificate_chain=None
                    # ),
                    options=[
                        ("grpc.keepalive_time_ms", 10000),
                        ("grpc.keepalive_timeout_ms", 5000),
                    ],
                )
                # Verify connection is actually working
                await self._channel.channel_ready()
                dispatch = await self.event_dispatcher.dispatch(
                    "connection_established",
                    {"address": self.address}
                )
                print(dispatch)
                return
            except grpc.RpcError as e:
                last_error = e 
                retry_count+=1
                await self.event_dispatcher.dispatch(
                    "connection_retry",
                    {
                        "address": self.address,
                        "attempt": retry_count,
                        "error": str(e)  
                    }
                )
                await asyncio.sleep(1 * retry_count) # Exponential backoff
        raise ConnectionError(
            f"Failed to connect to " + self.address + " after " + {self.max_retries} + " attempts"
        ) from last_error
    async def get_stub(self,service_name: str,stub_class):
        """Get or create a gRPC stub with lazy initialization"""
        if service_name not in self._stubs:
            if self._channel is None:
                await self.connect()
            self._stubs[service_name] = stub_class(self._channel)
        return self._stubs[service_name]
    async def close(self):
        """
        Cleanly close the connection
        """
        if self._channel is not None:
            await self._channel.close()
            self._channel=None
            self._stubs.clear()
            await self.event_dispatcher.dispatch(
                "connection_closed",
                {"address": self.address}
            )
    async def __aenter__(self):
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()