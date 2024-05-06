from django.db import models
from vendor_app.custom_helpers.model_serializers_helpers import AddCommonField, CustomUpdateManager
from .vendor_detail_model import VendorDetail


class CommonPurchaseOrder(AddCommonField):

    id = models.BigAutoField(primary_key=True) 
    vendor = models.ForeignKey(to=VendorDetail, related_name='vendor_purchase_orders', on_delete=models.RESTRICT, null=False)
    po_number = models.CharField(max_length=100, null=False, unique=True)
    order_date = models.DateTimeField(null=False)
    delivery_date = models.DateTimeField(null=False)
    items = models.JSONField(null=False)
    quantity = models.IntegerField(null=True)
    current_status = models.IntegerField(null=False)
    quality_rating = models.IntegerField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True)
    
    class Meta:
        abstract = True

class PurchaseOrder(CommonPurchaseOrder):

    class Meta:
        db_table = "vm_purchase_order"
        ordering = ('-creation_date',)

