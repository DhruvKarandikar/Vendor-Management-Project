from django.db import models
from vendor_app.custom_helpers.model_serializers_helpers import AddCommonField
from django.core.validators import MaxValueValidator

class CommonVendorDetail(AddCommonField):

    id = models.BigAutoField(primary_key=True)
    vendor_name = models.TextField(null=False)
    contact_details = models.TextField(null=False)
    vendor_code = models.CharField(max_length=100, null=False, unique=True)
    on_time_delivery_rate = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(10000)])
    quality_rating_avg = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(10000)])
    average_response_time = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(10000)])
    fulfillment_rate = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(10000)])

    class Meta:
        abstract = True


class VendorDetail(CommonVendorDetail):

    class Meta:
        db_table = "vm_vendor_detail"
        ordering = ('-creation_date',)

