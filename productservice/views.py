from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import grpc
from productservice.product_grpc import product_pb2, product_pb2_grpc  # generated files
from productservice.internal.app_service import ProductAppService


class ProductInfoView(APIView):

    def get(self, request, **kwargs):
        service = ProductAppService()
        product_id = kwargs.get("pk")
        # print(product_id)
        try:
            grpc_response = service.retrieve(id=product_id)
            if grpc_response is None:
                return Response(
                    {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "id": grpc_response.id,
                    "name": grpc_response.name,
                    "price": grpc_response.price,
                }
            )

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return Response(
                    {"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductListView(APIView):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def post(self, request):
        data = request.data
        service = ProductAppService()
        try:
            grpc_response = service.create(payload=data)
            return Response(
                {
                    "id": grpc_response.id,
                    "name": grpc_response.name,
                    "price": grpc_response.price,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, **kwargs):
        service = ProductAppService()
        grpc_response = service.list()

        # Make sure grpc_response is a list or iterable and serialize it
        if isinstance(grpc_response, list):
            serialized_data = [
                {"id": item.id, "name": item.name, "price": item.price}
                for item in grpc_response
            ]
        else:
            serialized_data = []

        return Response({"data": serialized_data}, status=status.HTTP_200_OK)
