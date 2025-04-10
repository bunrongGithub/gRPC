# Best Structure for Django Microservice Project Using REST and gRPC

A well-organized microservice architecture using Django should separate concerns clearly while making inter-service communication seamless. Here's an optimal structure for a system that uses REST for client-facing APIs and gRPC for service-to-service communication:

## Project Structure

```
microservices-project/
├── microservice/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── microservice/                         # Django project root
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── handlers.py                   # gRPC service registration
│   ├── product-app/                             # Django app 
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── api/                          # REST API components
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── grpc/                         # gRPC components
│   │   │   ├── __init__.py
│   │   │   ├── proto/                    # Proto definitions
│   │   │   │   └── service1.proto
│   │   │   ├── generated/                # Generated gRPC code
│   │   │   │   ├── __init__.py
│   │   │   │   ├── service1_pb2.py
│   │   │   │   └── service1_pb2_grpc.py
│   │   │   ├── serializers.py            # Proto serializers
│   │   │   └── services.py               # gRPC service implementations
│   │   └── clients/                      # Client code for other services
│   │       ├── __init__.py
│   │       └── service2_client.py
│   └── scripts/
│       └── generate_protos.sh
├── service-2/
│   # Similar structure as service-1
├── api-gateway/                          # Optional gateway service
├── proto-contracts/                      # Shared proto definitions
│   └── service1.proto
│   └── service2.proto
└── docker-compose.yml
```


import os
import subprocess
import sys
from django.core.management.base import BaseCommand

APP_CONFIG = {
    "auth": {
        "proto": "authservice/protos/auth.proto",
        "out": "authservice/auth_grpc",
        "proto_dir": "authservice/protos"
    },
    "order": {
        "proto": "orderservice/protos/order.proto",
        "out": "orderservice/order_grpc",
        "proto_dir": "orderservice/protos"
    },
    "product":{
        "proto":"productservice/protos/product.proto",
        "out":"productservice/product_grpc",
        "proto_dir":"productservice/protos"
    }
}


class Command(BaseCommand):
    help = "Compile .proto files for selected apps"

    def add_arguments(self, parser):
        parser.add_argument(
            "--auth", action="store_true", help="Compile proto for auth app"
        )
        parser.add_argument(
            "--order", action="store_true", help="Compile proto for order app"
        )
        parser.add_argument(
            "--product",action="store_true", help="Compile proto for order app"
        )
    def handle(self, *args, **options):
        selected_apps = [app for app in APP_CONFIG if options[app]]

        if not selected_apps:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️ No app specified. Use --auth or --order"
                )
            )
            return

        for app in selected_apps:
            config = APP_CONFIG[app]
            proto_file = config["proto"]
            out_path = config["out"]
            proto_dir = config["proto_dir"]
            
            # Ensure output directory exists
            os.makedirs(out_path, exist_ok=True)
            
            # Build the protoc command
            command = (
                f'{sys.executable} -m grpc_tools.protoc '
                f'-I{proto_dir} '
                f'--python_out={out_path} '
                f'--grpc_python_out={out_path} '
                f'{proto_file}'
            )
            
            self.stdout.write(f"Compiling {proto_file} for '{app}' app...")
            self.stdout.write(f"Command: {command}")
            
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully built gRPC files for '{app}'")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to build gRPC for '{app}'")
                    )
                    self.stderr.write(result.stderr)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error occurred while processing '{app}'")
                )
                self.stderr.write(str(e))