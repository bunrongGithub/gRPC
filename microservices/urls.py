"""
URL configuration for microservices project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from productservice.views import ProductInfoView, ProductListView
from handlers.service_handlers import grpc_handlers

def grpc_handler(server):
    grpc_handlers(server=server)


# from productservice.views import ProductInfoView,ProductList
urlpatterns = [
    path("api/products/<int:pk>", view=ProductInfoView.as_view()),
    path("api/products", view=ProductListView.as_view()),
    path("admin/", admin.site.urls),
    path("",include("orderservice.urls"))
]
