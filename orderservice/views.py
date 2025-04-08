from django_grpc_framework import generics
from rest_framework import viewsets
from orderservice.models import Order
from productservice.models import Product
from .serailizers import OrderProtoSerializer
from django.contrib.auth.models import User
# Create your views here.
class OrderService(generics.ModelService):
    queryset = Order.objects.all()
    serializer_class = OrderProtoSerializer
    def Create(self, request, context):

        return super().Create(request, context)
    def Update(self, request, context):
        return super().Update(request, context)