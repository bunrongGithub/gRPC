from django.db import models
from django.contrib.auth.models import User
from productservice.models import Product

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="order_user"
    )
    product = models.ForeignKey(
        to=Product, related_name="order_product", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "order"
