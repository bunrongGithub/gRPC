from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Payment
from client.order_client import OrderGRPCClient

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class PaymentSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField(read_only=True)
    order_data = serializers.SerializerMethodField(read_only=True)
    amount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Payment
        fields = [
            "id", "order", "order_data", "user", "user_data",
            "amount", "payment_method", "payment_status",
            "transaction_id", "created_at", "updated_at"
        ]

    def grpc_order_client(self):
        return OrderGRPCClient()

    def get_user_data(self, obj):
        try:
            user = User.objects.get(id=obj.user)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return {"error": "User not found"}

    def get_order_data(self, obj):
        try:
            return self.grpc_order_client().retrieve(order_id=obj.order)
        except Exception as e:
            return {"error": str(e)}
    def get_amount(self, obj):
        try:
            order = self.get_order_data(obj)
            return order.get('product', {}).get('price', None)
        except Exception as e:
            return None
