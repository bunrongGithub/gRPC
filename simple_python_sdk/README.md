# gRPC Saga Orchestrator SDK

Python SDK for implementing Saga Pattern with gRPC

## Installation

```bash
pip install grpc_saga_sdk
```

## Quick Start

### 1. Implement Participant Service

```python
from saga_orchestrator import service_base
import saga_pb2

class InventoryService(service_base.SagaParticipantBase):
    def execute(self, request, context):
        if request.headers.get("method") == "ReserveInventory":
            return self._reserve_inventory(request)
        return saga_pb2.SagaParticipantResponse(success=False)

    def compensate(self, request, context):
        if request.headers.get("method") == "ReleaseInventory":
            return self._release_inventory(request)
        return saga_pb2.SagaParticipantResponse(success=False)

    def _reserve_inventory(self, request):
        # Your implementation
        return saga_pb2.SagaParticipantResponse(success=True)

    def _release_inventory(self, request):
        # Compensation logic
        return saga_pb2.SagaParticipantResponse(success=True)
```

### 2. Run Participant Service

```python
from saga_orchestrator.service_base import run_participant_server

service = InventoryService()
run_participant_server(service, port=50052)
```

### 3. Use Orchestrator Client

```python
from saga_orchestrator.client import SagaClient

client = SagaClient()

# Define your saga steps
steps = [
    {
        "service": "localhost:50052",
        "method": "ReserveInventory",
        "compensation": "ReleaseInventory",
        "timeout": 5
    }
]

# Start a saga
response = client.start_saga(
    saga_id="order_123",
    steps=steps,
    payload={"order_id": "123", "items": ["item1"]}
)

print(response)
```


Client SDK Usage:
1. Initialize client
   client = SagaClient(orchestrator_host="localhost")

2. Define saga steps
   steps = [{
     'service': 'inventory:50052',
     'method': 'ReserveItem',
     'compensation': 'ReleaseItem'
   }]

3. Start saga
   saga = client.start_saga(
     saga_id="order_123",
     steps=steps,
     payload={"items": [...]}
   )

4. Check status
   status = client.get_saga_status("order_123")
   print(status['steps'][0]['result'])  # Access result payload

Participant Service Implementation:
class InventoryService(SagaParticipantBase):
    def execute(self, request):
        if request.headers['method'] == 'ReserveItem':
            # Business logic
            return SagaResponse(
                success=True,
                result_payload=json.dumps({"reserved": [...]}).encode()
            )

    def compensate(self, request):
        if request.headers['method'] == 'ReleaseItem':
            # Rollback logic
            return SagaResponse(success=True)

Orchestrator Internals:
• Maintains saga state
• Executes steps sequentially
• Triggers compensation on failure
• Persists execution history
• Provides status updates

Error Handling Flow:
1. Service fails → returns success=False
2. Orchestrator:
   - Marks step as failed
   - Initiates compensation
   - Executes reverse compensation flow
   - Updates saga status (COMPENSATED/FAILED)

Monitoring:
• All steps include:
  - Timestamps
  - Execution status
  - Result payloads
  - Error messages


  # 1. Import SDK
from saga_sdk import SagaClient

# 2. Initialize client
client = SagaClient(host="orchestrator.prod")

# 3. Define transaction
steps = [
    {
        "service": "payments:50051",
        "method": "ChargeCard",
        "compensation": "RefundPayment",
        "timeout": 10
    }
]

# 4. Execute
response = client.start_saga(
    saga_id="txn_789",
    steps=steps,
    payload={"amount": 100, "currency": "USD"}
)

# 5. Monitor
status = client.get_status("txn_789")


from saga_sdk.service_base import SagaParticipantBase

class PaymentService(SagaParticipantBase):
    def execute(self, request):
        # Implement business logic
        return self.success_result(
            transaction_id="txn_123",
            status="processed"
        )
    
    def compensate(self, request):
        # Implement rollback
        return self.success_result(
            refund_id="ref_456"
        )
    
    def success_result(self, **data):
        return self.Response(
            success=True,
            result_payload=json.dumps(data).encode()
        )