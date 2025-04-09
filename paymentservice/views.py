from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .models import Payment
from .serializers import PaymentSerializer
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class PaymentViewSet(viewsets.ModelViewSet):
    pagination_class=LargeResultsSetPagination
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer