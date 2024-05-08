from vendor_app.custom_helpers.status_code import *
from vendor_app.custom_helpers.model_serializers_helpers import CustomExceptionHandler
from vendor_app.models import *
from vendor_app.custom_helpers.model_serializers_helpers import create_update_model_serializer

def get_vendor_performance_service(request_data): 
    from vendor_app.serializers.vendor_serializer import HeadVendorPerformanceSerializer

    obj_id = request_data.get('id', None)
    vendor_performance_obj = VendorPerformance.objects.filter(id=obj_id).first()
    
    obj = []

    if vendor_performance_obj:
        serialized_obj = HeadVendorPerformanceSerializer(vendor_performance_obj)
        obj = serialized_obj.data

    return get_response(success, data=obj)

def delete_vendor_detail_service(request_data):
    
    obj_id = request_data.get('id', None)
    vendor_detail_obj = VendorDetail.objects.filter(id=obj_id).first()
    
    if not vendor_detail_obj:
        raise CustomExceptionHandler(no_object_exist)
    
    vendor_detail_obj.status = 0
    vendor_detail_obj.save()

    return get_response(success)


def get_vendor_detail_service(request_data):

    from vendor_app.serializers.vendor_serializer import HeadVendorDetailSerializer

    obj_id = request_data.get('id', None)
    search_object = request_data.get('search_object', None)

    vendor_detail_obj = VendorDetail.objects.filter(id=obj_id, status=1)
    
    if search_object == 'single' and not obj_id:
        raise CustomExceptionHandler(invalid_request_pass_id)

    if search_object == 'all':
        vendor_detail_obj = VendorDetail.objects.all()

    obj = []

    if vendor_detail_obj:
        obj_serializer = HeadVendorDetailSerializer(vendor_detail_obj, many=True)
        obj = obj_serializer.data

    return get_response(success, obj)


def vendor_detail_create_update_service(request_data):
    from vendor_app.serializers.vendor_serializer import VendorDetailCreateUpdateSerializer, HeadVendorPerformanceSerializer, HeadVendorDetailSerializer
    # from vendor_app.serializers.purchase_serializer import HeadPurchaseOrderSerializer

    vendor_performance_list = request_data.pop('vendor_performances', [])
    # vendor_purchase_list = request_data.pop('vendor_purchase_order', [])

    final_data = {}

    instance_vendor_detail = create_update_model_serializer(HeadVendorDetailSerializer,request_data,partial=True)

    if vendor_performance_list:

        for performance in vendor_performance_list:
            create_update_model_serializer(HeadVendorPerformanceSerializer, performance, partial=True, additional_data={'vendor_id': instance_vendor_detail.id})

    # if vendor_purchase_list:
    #     for purchase in vendor_purchase_list:
    #         create_update_model_serializer(HeadPurchaseOrderSerializer, purchase, partial=True, additional_data={'vendor_id': instance_vendor_detail.id})

    instance_vendor_detail_data = VendorDetailCreateUpdateSerializer(instance_vendor_detail).data
    final_data.update(instance_vendor_detail_data)

    return get_response(success, data=final_data)

