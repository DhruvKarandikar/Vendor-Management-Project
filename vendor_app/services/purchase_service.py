from vendor_app.custom_helpers.status_code import *
from vendor_app.custom_helpers.model_serializers_helpers import CustomExceptionHandler, create_update_model_serializer
from vendor_app.models import *
from vendor_app.signals.purchase_signal import update_performance_metrics


def get_purchase_service(request_data):

    # Because of serializer not importing and giving out error --> Do not Remove
    from vendor_app.serializers.purchase_serializer import HeadPurchaseOrderSerializer

    obj_id = request_data.get('id', None)
    search_object = request_data.get('search_object', None)
    vendor_id = request_data.get('vendor_id', None)

    purchase_obj = PurchaseOrder.objects.all()

    if search_object == 'all':
        purchase_obj = PurchaseOrder.objects.all()

    if search_object == 'single' and obj_id:
        purchase_obj = purchase_obj.filter(id=obj_id, status=1)          

    if vendor_id:
        purchase_obj = purchase_obj.filter(vendor_id=vendor_id)

    obj = []

    if purchase_obj:
        obj_serializer = HeadPurchaseOrderSerializer(purchase_obj, many=True)
        obj = obj_serializer.data

    return get_response(success, obj)



def delete_purchase_object_service(request_data):

    obj_id = request_data.get('id', None)
    prchase_obj = PurchaseOrder.objects.filter(id=obj_id).first()
    
    if not prchase_obj:
        raise CustomExceptionHandler(no_object_exist)

    prchase_obj.status = 0
    prchase_obj.save()

    return get_response(success)


def purchase_create_update_service(request_data):

    from vendor_app.serializers.purchase_serializer import PurchaseOrderRequestSerailizer
    
    final_data = []

    for data in request_data:

        instance_vendor_detail = create_update_model_serializer(PurchaseOrderRequestSerailizer,data,partial=True)
        instance_vendor_detail = update_performance_metrics(sender=PurchaseOrder, instance=instance_vendor_detail)
        final_data.append(instance_vendor_detail)

    return get_response(success, data=PurchaseOrderRequestSerailizer(final_data, many=True).data)


