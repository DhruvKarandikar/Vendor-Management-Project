from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from vendor_app.models import PurchaseOrder
from django.db.models import Avg
from datetime import timezone
from vendor_app.custom_helpers.consts import current_status_po


@receiver(post_save, sender=PurchaseOrder, dispatch_uid="update_performance_metrics")
def update_performance_metrics(sender, instance, **kwargs):

    vendor = instance.vendor
    common_query = PurchaseOrder.objects.filter(vendor=vendor)
    COMPLETE = current_status_po.get('completed')

    if instance.status == COMPLETE:
        delivered_on_time_count = common_query.filter(current_status=COMPLETE, delivery_date__lte=timezone.now()).count()
        if common_query.exists():
            on_time_delivery_rate = delivered_on_time_count / common_query.count() * 100
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.save()

        total_po_count = common_query.count()
        fulfilled_po_count = common_query.filter(current_status=COMPLETE).exclude(quality_rating__lt=1).count()

        if total_po_count > 0:
            fulfilment_rate = (fulfilled_po_count / total_po_count) * 100
            vendor.fulfilment_rate = fulfilment_rate
            vendor.save()

    if instance.quality_rating is not None:
        average_quality_rating = common_query.filter(current_status=COMPLETE).aggregate(quality_rating=Avg('quality_rating'))['quality_rating']
        vendor.quality_rating_avg = average_quality_rating
        vendor.save()

    if instance.acknowledgment_date is not None:

        acknowledged_pos = common_query.filter(current_status=COMPLETE, acknowledgment_date__isnull=False)

        total_response_time = 0
        for po in acknowledged_pos:
            response_time = po.acknowledgment_date - po.issue_date
            total_response_time += response_time.total_seconds()

        if acknowledged_pos.exists():
            average_response_time_seconds = total_response_time / acknowledged_pos.count()
            average_response_time_hours = average_response_time_seconds / 3600
            vendor.average_response_time = average_response_time_hours
            vendor.save()
    
    return instance
    


