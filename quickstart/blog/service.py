import grpc
from google.protobuf import empty_pb2
from django_grpc_framework.services import Service

from blog.models import Post
from blog.serializer import PostProtoSerializer


class PostService(Service):
    def List(self, request, context):
        post = Post.objects.all()
        serializer = PostProtoSerializer(post, many=True)
        for msg in serializer.message:
            yield msg

    def Create(self, request, context):
        serializer = PostProtoSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND)
