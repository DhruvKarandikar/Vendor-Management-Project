from django.db import models
from vendor_app.custom_helpers.model_serializers_helpers import AddCommonField, CustomUpdateManager
from .vendor_detail_model import VendorDetail


class CommonVendorPerformance(AddCommonField):

    id = models.BigAutoField(primary_key=True) 
    vendor = models.ForeignKey(to=VendorDetail, related_name='performance', on_delete=models.RESTRICT, null=False)
    date =  models.DateTimeField(null=False)
    on_time_delivery_rate =  models.IntegerField(null=False)
    quality_rating_avg = models.IntegerField(null=False)
    average_response_time = models.IntegerField(null=False)
    fulfillment_rate = models.IntegerField(null=False)

    class Meta:
        abstract = True

class VendorPerformance(CommonVendorPerformance):

    class Meta:
        db_table = "vm_vendor_performance"
        ordering = ('-creation_date',)

