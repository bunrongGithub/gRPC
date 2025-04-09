from rest_framework import viewsets
from .models import Order
from .serailizers import OrderSerializer
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class=OrderSerializer

    def perform_create(self, serializer):
        serializer.save(self.request.user)
        return super().perform_create(serializer)