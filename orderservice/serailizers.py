from .models import Order
from rest_framework import serializers
from django.contrib.auth.models import User

# from client.retrieve import retrieve
from client.grpc_product_client import ProductGRPCClient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def grpc_product_client(self):
        return ProductGRPCClient()

    def get_product(self, object):
        try:
            product = self.grpc_product_client().retrieve(product_id=object.product.id)
            return product
        except Exception as e:
            raise e
