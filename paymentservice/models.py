from django.db import models

class Payment(models.Model):
    order = models.IntegerField()
    user = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    payment_method = models.CharField(max_length=50, choices=[('card', 'Card'), ('paypal', 'PayPal'), ('bank', 'Bank Transfer')])
    payment_status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='pending'
    )
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment"

    def __str__(self):
        return f"Payment for Order {self.order.id if self.order else 'N/A'} - Status: {self.payment_status}"
