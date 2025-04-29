
from typing import Any
from simple_python_sdk.core.connection.manager import ConnectionManager


class GrpcSDKConnection:
    def __init__(self, grpc_server_add: str):
        self.conn_manager = ConnectionManager(grpc_server_add)
    def __enter__(self):
        self.conn_manager.connect()
        return self
        
    def __exit__(self,**kwargs):
        self.conn_manager.close()