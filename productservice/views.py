from rest_framework.views import APIView
from rest_framework.response import Response
import grpc
from django import http
from productservice.product_grpc import product_pb2, product_pb2_grpc  # import generated stubs

class ProductInfoView(APIView):
    
    def get(self, request, format=None):
        product_id = int(request.query_params.get('id', 1))  # e.g. ?id=5
        
        # Set up gRPC channel & stub
        channel = grpc.insecure_channel('localhost:50051')
        stub = product_pb2_grpc.ProductServiceStub(channel)

        # Build request & call the RPC
        grpc_request = product_pb2.ProductRequest(id=product_id)
        
        # Set timeout to prevent hanging indefinitely
        grpc_response = stub.GetProduct(grpc_request, timeout=10)  # 10 seconds timeout
        if not grpc_response:
            return http.HttpResponseNotFound
        # Return REST-style JSON response
        return Response({
            'id': grpc_response.id,
            'name': grpc_response.name,
            'price': grpc_response.price
        })
    
class ProductList(APIView):
    def list(self,request):
        channel = grpc.insecure_channel("localhost:50051")
        stub = product_pb2_grpc.ProductServiceStub(channel)
        grpc_response = stub.ListProducts()

        return Response({grpc_response})