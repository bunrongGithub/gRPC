from core_sdk.core_sdk.message import add_outbox_message
from .models import Order
from rest_framework import serializers
from django.contrib.auth.models import User


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

    # def get_product(self, object):
    #     try:
    #         product = self.grpc_product_client().retrieve(product_id=object.product.id)
    #         return product
    #     except Exception as e:
    #         raise e

    def get_product(self,object):
        try:
            add_outbox_message(
                service="product",
                payloard={
                    "action": "get_product",
                    "product_id": object.product.id
                }
            )
            return {"status": "queued", "message": "Product retrieval scheduled"}
        except Exception as e:
            return {"error": str(e)}