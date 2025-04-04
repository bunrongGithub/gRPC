from django.contrib.auth.models import User
from authservice import auth_pb2 as pb2, auth_pb2_grpc as pb2_grpc
from django.contrib.auth.hashers import make_password,check_password


class AuthService(pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        if User.objects.filter(username=request.username).exists():
            return pb2.RegisterResponse(message="User already exists")
        user = User(username=request.username,password=make_password(request.password))
        user.save()
        return pb2.RegisterResponse(message="User Registerd successfully!")
    def Login(self, request, context):
        user = User.objects.filter(username=request.username).first()
        if user and check_password(request.password,user.password):
            return pb2.LoginResponse(token="token")
        return pb2.LoginResponse(token="")
