import grpc
from django.conf import settings
class GRPCClient:
    def __init__(self,service_name):
        self.service_name=service_name
        self.channel=None
    def __enter__(self):
        service_url = getattr(settings,f"{self.service_name.upper()}_SERVICE_URL")
        self.channel = grpc.insecure_channel(service_url)
    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.channel:
            self.channel.close()