import grpc
from productservice.product_grpc import product_pb2 as pb2, product_pb2_grpc as pb2_grpc
import logging

def run():
    # Enable gRPC debugging
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            
            stub = pb2_grpc.ProductServiceStub(channel=channel)
            response_stream = stub.ListProducts(pb2.ProductListRequest())
            print(response_stream) 
    except grpc.RpcError as e:
        print(e)
        print(f"gRPC error occurred: {e.code().name}: {e.details()}")
        if e.code() == grpc.StatusCode.UNIMPLEMENTED:
            print("Make sure the server has implemented this method")
        elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            print("Request timed out. Is the server responding?")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    run()