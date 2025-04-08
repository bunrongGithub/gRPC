from django_grpc_framework import proto_serializers
from orderservice.models import Order
from orderservice.order_grpc import order_pb2

class OrderProtoSerializer(proto_serializers.ModelProtoSerializer):
    
    class Meta:
        model=Order
        proto_class = order_pb2.OrderResponse
        fields="__all__"