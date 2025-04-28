from django.contrib.auth.models import User
from django_grpc_framework.generics import ModelService
from account.serializers import UserProtoSerializer

class UserService(ModelService):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class=UserProtoSerializer
