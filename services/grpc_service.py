from productservice.product_grpc import product_pb2_grpc
# Import Product Model
from productservice.models import Product
class ProductService(product_pb2_grpc.ProductServiceServicer):
    def GetProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
            return product
        except Product.DoesNotExist as e:
            print("Product not found!!")
    def ListProducts(self, request, context):
        return Product.objects.all().order_by("name")