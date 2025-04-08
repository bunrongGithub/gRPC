from django_grpc_framework.services import Service
import grpc
from productservice.models import Product
from productservice.serializers import ProductProtoSerializer


class ProductService(Service):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, "Product:%s not found!" % pk)

    def GetProduct(self, request, context):
        product = self.get_object(request.id)
        serializer = ProductProtoSerializer(product)
        return serializer.message

    def ListProducts(self, request, context):
        products = Product.objects.all()
        serializer = ProductProtoSerializer(products, many=True)
        for msg in serializer.message:
            yield msg
