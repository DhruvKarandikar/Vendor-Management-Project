from django.db import models
from vendor_app.custom_helpers.model_serializers_helpers import AddCommonField, CustomUpdateManager

class CommonVendorDetail(AddCommonField):

    id = models.BigAutoField(primary_key=True)
    vendor_name = models.TextField(null=False)
    contact_details = models.TextField(null=False)
    vendor_code = models.CharField(max_length=100, null=False, unique=True)
    on_time_delivery_rate = models.PositiveIntegerField(null=False)
    quality_rating_avg = models.PositiveIntegerField(null=False)
    average_response_time = models.PositiveIntegerField(null=False)
    fulfillment_rate = models.PositiveIntegerField(null=False)

    class Meta:
        abstract = True


class VendorDetail(CommonVendorDetail):
    
    CustomUpdateManager.set_logModel(logModel="VendorDetailLog",  model="VendorDetail")

    class Meta:
        db_table = "vm_vendor_detail"
        ordering = ('-creation_date',)


class VendorDetailLog(CommonVendorDetail):
    
    vendor_detail_log = models.ForeignKey(to=VendorDetail, on_delete=models.SET_NULL, null=True, related_name='logs')
    updation_by = None
    updation_date = None

    class Meta:
        db_table = "vm_vendor_detail_log"
        ordering = ('-creation_date',)


