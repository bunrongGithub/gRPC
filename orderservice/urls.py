from django.urls import path, include
from rest_framework import routers
from .views import OrderViewSet

routes = routers.DefaultRouter()
routes.register("orders", viewset=OrderViewSet)
urlpatterns = [path("api/v1/", include(routes.urls))]
