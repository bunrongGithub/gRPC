from django.contrib.auth.models import User
from django_grpc_framework.proto_serializers import ModelProtoSerializer
import account.account_pb2 as account__pb2


class UserProtoSerializer(ModelProtoSerializer):
    class Meta: 
        model=User
        proto_class = account__pb2.User
        fields = ['id', 'username', 'email', 'groups']
