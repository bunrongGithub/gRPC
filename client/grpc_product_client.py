from client.grpc_client import GRPCClient
from productservice.product_grpc import product_pb2 as pb2, product_pb2_grpc as pb2_grpc


class ProductGRPCClient:
    def retrieve(self,product_id):
        with GRPCClient("product") as channel:
            stub = pb2_grpc.ProductServiceStub(channel)
            request = pb2.ProductRequest(id=product_id)
            response = stub.GetProduct(request)
            return {"id": response.id, "name": response.name, "price": response.price}

    def list(self):
        with GRPCClient("product") as channel:
            stub = pb2_grpc.ProductServiceStub(channel)
            response = stub.ListProducts(pb2.ProductListRequest())
            return [
                {"id": p.id, "name": p.name, "price": p.price}
                for p in response.products
            ]
#Test
if __name__ == "__main__":
    called = ProductGRPCClient()
    print(called.retrieve(4))
    print(called.list())