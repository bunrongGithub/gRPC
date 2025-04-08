from django_grpc_framework import proto_serializers
from authservice.models import Product

from product_grpc import product_pb2 as pb2

class ProductProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model=Product
        proto_class=pb2.Product
        fields="__all__"

    