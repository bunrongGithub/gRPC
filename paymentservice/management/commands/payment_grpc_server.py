import grpc 

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = "Start gRPC Server"
    def handle(self, *args, **options):
        return super().handle(*args, **options)
