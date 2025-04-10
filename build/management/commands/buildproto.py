import os
import subprocess
import sys
from django.core.management.base import BaseCommand

APP_CONFIG = {
    "auth": {
        "proto": "authservice/protos/auth.proto",
        "out": "authservice/auth_grpc",
        "proto_dir": "authservice/protos",
    },
    "order": {
        "proto": "orderservice/protos/order.proto",
        "out": "orderservice/order_grpc",
        "proto_dir": "orderservice/protos",
    },
    "product": {
        "proto": "productservice/protos/product.proto",
        "out": "productservice/product_grpc",
        "proto_dir": "productservice/protos",
    },
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
            "--product", action="store_true", help="Compile proto for order app"
        )

    def handle(self, *args, **options):
        selected_apps = [app for app in APP_CONFIG if options[app]]

        if not selected_apps:
            self.stdout.write(
                self.style.WARNING("⚠️ No app specified. Use --auth or --order")
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
                f"{sys.executable} -m grpc_tools.protoc "
                f"-I {proto_dir} "
                f"--python_out={out_path} "
                f"--grpc_python_out={out_path} "
                f"{proto_file}"
            )

            self.stdout.write(f"Compiling {proto_file} for '{app}' app...")
            self.stdout.write(f"Command: {command}")

            try:
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True
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
