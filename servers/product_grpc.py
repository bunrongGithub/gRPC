import grpc
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microservices.settings")
django.setup()

import productservice.product_grpc.product_pb2 as pb2
import productservice.product_grpc.product_pb2_grpc as pb2_grpc
from productservice.models import Product
from concurrent import futures


class ProductService(pb2_grpc.ProductServiceServicer):
    def ListProducts(self, request, context):
        products = Product.objects.all()

        # Build list of Product messages
        product_messages = []
        for product in products:
            product_messages.append(
                pb2.Product(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                )
            )

        return pb2.ProductList(products=product_messages)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
