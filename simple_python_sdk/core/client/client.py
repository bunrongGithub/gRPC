import base64
import json
import grpc
import saga_pb2
import saga_pb2_grpc
from google.protobuf.json_format import MessageToDict

class GrpcOrchestratorClient:
    def __init__(self, orchestrator_host='localhost', orchestrator_port=50051):
        self.orchestrator_address = f"{orchestrator_host}:{orchestrator_port}"
        print(self.orchestrator_address)
    def start_transaction(self, transaction_id: str, steps: list, payload: dict={}) -> dict:
        """Start a new grpc transaction with explicit service ports"""
        try:
            # Convert steps to use explicit ports
            saga_steps = []
            for step in steps:
                print(step['port'])
                saga_steps.append(saga_pb2.SagaStep(
                    service_name=f"localhost:{step['port']}",  # Explicit port
                    rpc_method=step['rpc_method'],
                    compensation_method=step['compensation_method'],
                    timeout_seconds=step.get('timeout_seconds', 5)
                ))
            with grpc.insecure_channel(self.orchestrator_address) as channel:
                print("connect to base transaction on port - ",self.orchestrator_address)
                stub = saga_pb2_grpc.SagaOrchestratorServiceStub(channel)
                response = stub.StartSaga(saga_pb2.StartSagaRequest(
                    saga_id=transaction_id,
                    steps=saga_steps,
                    payload=str(payload).encode()
                ))
                print("3 - ",response)
                return MessageToDict(response)
        except grpc.RpcError as e:
            print(f"Error starting saga: {e.code()}: {e.details()}")
            return None

    def get_saga_status(self, saga_id: str) -> dict:
        try:
            with grpc.insecure_channel(self.orchestrator_address) as channel:
                stub = saga_pb2_grpc.SagaOrchestratorServiceStub(channel)
                response = stub.GetSagaStatus(
                    saga_pb2.GetSagaStatusRequest(saga_id=saga_id)
                )
                
                response_dict = MessageToDict(response)

                if 'steps' in response_dict:
                    for step in response_dict['steps']:
                        if 'resultPayload' in step:
                            try:
                                raw = base64.b64decode(step['resultPayload'])
                                step['resultPayload'] = json.loads(raw.decode('utf-8'))
                            except Exception as e:
                                raise e
                return response_dict
        except grpc.RpcError as e:
            print(f"Error getting status: {e.code()}: {e.details()}")
            return None
if __name__ == '__main__':
    client = GrpcOrchestratorClient()
    steps = [
        # {
        #     'port': 50052,
        #     'rpc_method': 'ReserveInventory',
        #     'compensation_method': 'ReleaseInventory',
        #     'timeout_seconds': 5
        # },
        {
            'port': 50053,
            'rpc_method': 'RefundPayment',
            'compensation_method': 'RefundPayment',
            'timeout_seconds': 5
        }
    ]
    response = client.start_transaction(
        transaction_id="order_123",
        steps=steps,
    )
    print("Response:", response)
    status = client.get_saga_status(saga_id="order_123")
    
    print("Receive status:: ", status)