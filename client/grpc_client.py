import grpc
# from django.conf import settings
import os 
from dotenv import load_dotenv
load_dotenv()
class GRPCClient:
    def __init__(self, service_name):
        self.service_name = service_name
        self.channel = None

    def __enter__(self):
        service_url = os.getenv(f"{self.service_name.upper()}_SERVICE_URL")

        if not service_url:
            raise ValueError(f"No URL found for service: {self.service_name.upper()}_SERVICE_URL")
        
        self.channel = grpc.insecure_channel(service_url)
        return self.channel  

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.channel:
            self.channel.close()

