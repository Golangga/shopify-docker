from django.db import models

# Create your models here.
class PriceRule(models.Model):
    title = models.CharField(max_length=255)
    target_type = models.CharField(max_length=255)
    target_selection = models.CharField(max_length=255)
    allocation_method = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)
    value = models.IntegerField(null=True, blank=True)
    customer_segment_prerequisite = models.CharField(max_length=255, null=True, blank=True)
    prerequisite_quantity_range = models.PositiveIntegerField(null=True, blank=True)
    prerequisite_shipping_price_range = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prerequisite_subtotal_range = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prerequisite_to_entitlement_quantity_ratio = models.PositiveIntegerField(null=True, blank=True)
    prerequisite_to_entitlement_purchase = models.PositiveIntegerField(null=True, blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

  
class DiscountCode(models.Model):  
    code = models.CharField(max_length=20, unique=True)  
    created_at = models.DateTimeField()  
    updated_at = models.DateTimeField()  
    id = models.IntegerField(primary_key=True)  
    price_rule = models.ForeignKey('PriceRule', on_delete=models.CASCADE)  
    usage_count = models.IntegerField()  
    errors = models.TextField()  