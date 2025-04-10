import grpc
from concurrent import futures
from django.core.management.base import BaseCommand, CommandError
from productservice.product_grpc import product_pb2_grpc
from shared.services.product_service import ProductService


class Command(BaseCommand):
    help = "Start the gRPC server"
    def handle(self, *args, **options):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        product_pb2_grpc.add_ProductServiceServicer_to_server(servicer=ProductService(),server=server)
        server.add_insecure_port("[::]:50051")
        self.stdout.write(self.style.SUCCESS("Starting gRPC server on port 50051"))
        server.start()
        server.wait_for_termination()

