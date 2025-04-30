

from concurrent import futures
import logging

import grpc
import saga_pb2, saga_pb2_grpc


class ExampleService(saga_pb2_grpc.SagaParticipantServicer):
    def Execute(self, request, context):
        method = request.headers.get("step-method")
        self.logger = logging.getLogger(__name__)

        try:
            if method == "ReserveInventory":
                return self._reserve_inventory(request)
            elif method == "RefundPayment":
                return self._refund_payment(request)
            else:
                return saga_pb2.SagaParticipantResponse(
                    seccuess = False,
                    error_message = f"Unknown compensation {method}"
                )
        except Exception as e:
            self.logger.error(f"Compensation failed: {e}")
            return saga_pb2.SagaParticipantResponse(
                success=False,
                error_message=str(e)
            )

    def Compensate(self, request, context):
        method = request.headers.get("compensation-method")
        try:
            if method == "ReleaseInventory":
                return self._release_inventory(request=request)
            elif method == "RefundPayment":
                return self._refund_payment(request=request)
            else: 
                return saga_pb2.SagaParticipantResponse(
                    success = False,
                    error_message=f"Unknown compensation {method}"
                )
        except Exception as e:
            self.logger.error(f"Compensation failed: {e}")
            return saga_pb2.SagaParticipantResponse(
                success=False,
                error_message=str(e)
            )
    def _reserve_inventory(self, request):
        # Business logic here
        return saga_pb2.SagaParticipantResponse(success=True)
    
    def _process_payment(self, request):
        # Business logic here
        return saga_pb2.SagaParticipantResponse(success=True)
    
    def _release_inventory(self, request):
        # Compensation logic here
        return saga_pb2.SagaParticipantResponse(success=True)
    
    def _refund_payment(self, request):
        # Compensation logic here
        return saga_pb2.SagaParticipantResponse(success=True)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saga_pb2_grpc.add_SagaParticipantServicer_to_server(
        ExampleService(), server)
    server.add_insecure_port('[::]:50053')
    print("Example Service Starting at 50053")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()