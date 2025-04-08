#!/bin/bash

python -m grpc_tools.protoc -I./orderservice/protos --python_out=./orderservice/order_grpc --grpc_python_out=./orderservice/order_grpc orderservice/protos/order.proto
python -m grpc_tools.protoc -I./productservice/protos --python_out=./productservice/product_grpc --grpc_python_out=./productservice/product_grpc productservice/protos/product.proto
echo "gRPC code generation completed successfully!"