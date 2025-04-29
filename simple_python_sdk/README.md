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

