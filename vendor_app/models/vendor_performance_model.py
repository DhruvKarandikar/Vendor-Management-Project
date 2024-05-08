from django.db import models
from vendor_app.custom_helpers.model_serializers_helpers import AddCommonField, CustomUpdateManager
from .vendor_detail_model import VendorDetail
from django.core.validators import MaxValueValidator

class CommonVendorPerformance(AddCommonField):

    id = models.BigAutoField(primary_key=True) 
    vendor = models.ForeignKey(to=VendorDetail, related_name='vendor_performance', on_delete=models.RESTRICT, null=False)
    date =  models.DateTimeField(null=False)
    on_time_delivery_rate =  models.IntegerField(null=False, validators=[MaxValueValidator(10000)])
    quality_rating_avg = models.IntegerField(null=False, validators=[MaxValueValidator(10000)])
    average_response_time = models.IntegerField(null=False, validators=[MaxValueValidator(10000)])
    fulfillment_rate = models.IntegerField(null=False, validators=[MaxValueValidator(10000)])

    class Meta:
        abstract = True

class VendorPerformance(CommonVendorPerformance):

    class Meta:
        db_table = "vm_vendor_performance"
        ordering = ('-creation_date',)

