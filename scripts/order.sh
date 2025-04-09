#!/bin/bash

python -m grpc_tools.protoc -I./orderservice/protos --python_out=./orderservice/order_grpc --grpc_python_out=./orderservice/order_grpc orderservice/protos/order.proto
echo "gRPC code generation completed successfully!"