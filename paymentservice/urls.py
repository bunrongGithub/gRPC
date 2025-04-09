from django.urls import path, include
from rest_framework import routers
from .views import PaymentViewSet
routes = routers.DefaultRouter()
routes.register("payments",viewset=PaymentViewSet)

urlpatterns = [
    path("api/v1/", include(routes.urls))
]