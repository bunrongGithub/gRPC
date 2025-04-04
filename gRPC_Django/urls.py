"""
URL configuration for gRPC_Django project.

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
from django.urls import path
from authservice.services import auth_service as services
from django_grpc_framework import grpc_server

# Register your gRPC services
grpc_urls = [
    (services.AuthService, services.auth_pb2_grpc.add_AuthServiceServicer_to_server),
]

# Register the gRPC URLs to the server
grpc_server.register(grpc_urls)

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Optionally, if you want to serve the gRPC service directly within Django, you could add the following:
# path('grpc/', grpc_server.serve),

