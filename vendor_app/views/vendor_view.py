import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from vendor_app.custom_helpers.status_code import get_response, generic_error_2, log_info_message
from vendor_app.custom_helpers.model_serializers_helpers import CustomExceptionHandler
from vendor_app.serializers.vendor_serializer import *
from vendor_app.services.vendor_service import get_vendor_performance_service, delete_vendor_detail_service, \
                get_vendor_detail_service, vendor_detail_create_update_service
from vendor_app.custom_helpers.custom_decorator import custom_api_view

logger = logging.getLogger("django")

# Vendor API
@csrf_exempt
@custom_api_view(
    request_serializer=VendorDetailRequestDeleteSerailizer,
    responses={"200": DeleteVendorDetailResponseSerailizer},
    operation_id="Delete Vendor"
)
def delete_vendor(request):
    response_obj = None

    try:
        logger.info(request, "request for vendor delete")
        response_obj = delete_vendor_detail_service(request.validation_serializer.validated_data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in vendor delete url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in vendor delete url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in vendor delete --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)



@csrf_exempt
@custom_api_view(
    request_serializer=GetVendorDetailRequestSerializer,
    responses={"200": GetVendorDetailResponseSerializer},
    operation_id="Get Vendor"
)
def get_vendor(request):
    response_obj = None

    try:
        logger.info(request, "request for get vendor details")
        response_obj = get_vendor_detail_service(request.validation_serializer.validated_data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in get vendor details url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in get vendor details url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in get vendor details --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=VendorDetailCreateUpdateSerializer,
    responses={"200": VendorDetailCrudResponseSerializer},
    operation_id="Vendor Create Update"
)
@api_view(["POST"])
def vendor_create_update(request):
    response_obj = None

    try:
        logger.info(request, "request for vendor create update")
        response_obj = vendor_detail_create_update_service(request.data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in vendor crud url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in vendor crud url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in vendor crud --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


@csrf_exempt
@custom_api_view(
    request_serializer=GetVendorPerformanceRequestSerailizer,
    responses={"200": GetVendorPerformanceResponseSerailizer},
    operation_id="Get Vendor Performance"
)
def get_vendor_performance(request):
    response_obj = None

    try:
        logger.info(request, "request for vendor performance")
        response_obj = get_vendor_performance_service(request.validation_serializer.validated_data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in vendor performance url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in vendor performance url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in vendor performance --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)

