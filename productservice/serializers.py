from django_grpc_framework import proto_serializers
from productservice.models import Product
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","microservices.settings")
import django
django.setup()
import productservice.product_grpc.product_pb2 as product__pb2_grpc

class ProductProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model=Product
        proto_class=product__pb2_grpc.Product
        fields="__all__"

    