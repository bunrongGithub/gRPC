from django.contrib import admin
from django.urls import path
import account.account_pb2_grpc as account_pb2_grpc
from account.services import UserService
from blog.handlers import grpc_handlers as blog_grpc_app_handlers
from account.handlers import account_grpc_app_handler
# Regular HTTP URLs
urlpatterns = [
    path('admin/', admin.site.urls),
]

def grpc_handlers(server):
    """Register all gRPC handlers"""
    # Account service
    account_grpc_app_handler(server)
    
    # Blog service
    blog_grpc_app_handlers(server)