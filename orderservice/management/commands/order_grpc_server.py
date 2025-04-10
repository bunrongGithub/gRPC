import os
import grpc
from concurrent import futures
from django.core.management.base import BaseCommand
from orderservice.order_grpc import order_pb2_grpc
from shared.services.order_service import OrderService
GRPC_ORDER_HOST = os.getenv("GRPC_ORDER_HOST")


class Command(BaseCommand):
    help = "Start the gRPC server"
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        order_pb2_grpc.add_OrderServiceServicer_to_server(servicer=OrderService(),server=server)
        server.add_insecure_port(GRPC_ORDER_HOST)
        self.stdout.write(self.style.SUCCESS(f"Starting gRPC server on port {GRPC_ORDER_HOST}"))
        server.start()
        server.wait_for_termination()

