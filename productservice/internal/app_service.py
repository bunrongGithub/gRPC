# productservice/app_services.py
from productservice.models import Product
from productservice.serializers import ProductProtoSerializer


class ProductAppService:
    def retrieve(self, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return {"error": "Product not found"}  # You can return an error message or None
        except Exception as e:
            return {"error": str(e)}  # For any other unexpected errors
        serializer = ProductProtoSerializer(product)
        return serializer.message

    def create(self, payload):
        try:
            product = Product.objects.create(**payload)
        except Exception as e:
            return {"error": str(e)}  # Capture any exception during product creation
        serializer = ProductProtoSerializer(product)
        return serializer.message

    def list(self, request=None):
        try:
            products = Product.objects.all()
        except Exception as e:
            return {"error": str(e)}  # Capture any exception during listing
        serializer = ProductProtoSerializer(products, many=True)
        return serializer.message
