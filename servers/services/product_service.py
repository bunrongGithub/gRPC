import grpc
import os
# import django

# # Setup Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microservices.settings")
# django.setup()

import productservice.product_grpc.product_pb2 as pb2
import productservice.product_grpc.product_pb2_grpc as pb2_grpc
from productservice.models import Product


class ProductService(pb2_grpc.ProductServiceServicer):
    model = Product.objects.all()

    def get_query_set(self):
        return self.model

    def ListProducts(self, request, context):
        product_messages = []
        for product in self.get_query_set():
            product_messages.append(
                pb2.Product(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                )
            )

        return pb2.ProductList(products=product_messages)

    def GetProduct(self, request, context):
        try:
            product = self.get_query_set().get(id=request.id)
            return pb2.Product(
                id=product.id,
                name=product.name,
                price=product.price
            )
        except grpc.RpcError as e:
            raise e