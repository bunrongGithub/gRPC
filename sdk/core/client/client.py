import grpc
import saga_pb2
import saga_pb2_grpc
from google.protobuf.json_format import MessageToDict

class SagaClient:
    def __init__(self, orchestrator_host='localhost', orchestrator_port=50051):
        self.orchestrator_address = f"{orchestrator_host}:{orchestrator_port}"
    
    def start_transaction(self, transaction_id: str, steps: list, payload: dict) -> dict:
        """Start a new saga with explicit service ports"""
        try:
            # Convert steps to use explicit ports
            saga_steps = []
            for step in steps:
                saga_steps.append(saga_pb2.SagaStep(
                    service_name=f"localhost:{step['port']}",  # Explicit port
                    rpc_method=step['rpc_method'],
                    compensation_method=step['compensation_method'],
                    timeout_seconds=step.get('timeout_seconds', 5)
                ))
            
            with grpc.insecure_channel(self.orchestrator_address) as channel:
                stub = saga_pb2_grpc.SagaOrchestratorServiceStub(channel)
                response = stub.StartSaga(saga_pb2.StartSagaRequest(
                    saga_id=transaction_id,
                    steps=saga_steps,
                    payload=str(payload).encode()
                ))
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
                return MessageToDict(response)
        except grpc.RpcError as e:
            print(f"Error getting status: {e.code()}: {e.details()}")
            return None

if __name__ == '__main__':
    client = SagaClient()
    
    # Define services with explicit ports
    steps = [
        # {
        #     'port': 50052,  # Inventory service port
        #     'rpc_method': 'ReserveInventory',
        #     'compensation_method': 'ReleaseInventory',
        #     'timeout_seconds': 5
        # },
        {
            'port': 50053,  # Payment service port
            'rpc_method': 'ProcessPayment',
            'compensation_method': 'RefundPayment',
            'timeout_seconds': 5
        }
    ]
    
    print("Starting saga...")
    response = client.start_transaction(
        transaction_id="order_123",
        steps=steps,
        payload={"order_id": "123", "items": ["item1", "item2"]}
    )
    print("Response:", response)
    
    print("\nChecking status...")
    status = client.get_saga_status("order_123")
    print("Status:", status)