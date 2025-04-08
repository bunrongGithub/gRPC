from utils.grpc_client import GRPCClient
from productservice.product_grpc import product_pb2, product_pb2_grpc
from django_grpc_framework import generics
import grpc
class ProductService(generics.GenericService):
    def GetProduct(self, request, context):
        with GRPCClient('external_epp') as channel:
            stub = product_pb2_grpc.ExternalEPPServiceStub(channel)
            try:
                # Transform request if needed
                external_request = product_pb2.ExternalRequest(
                    product_id=request.id
                )
                response = stub.GetExternalProduct(external_request)
                return product_pb2.ProductResponse(
                    id=response.id,
                    name=response.name,
                    price=response.price
                )
            except grpc.RpcError as e:
                context.set_code(e.code())
                context.set_details(e.details())
                raise