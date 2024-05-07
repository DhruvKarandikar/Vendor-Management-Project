import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from vendor_app.custom_helpers.custom_decorator import custom_api_view
from vendor_app.custom_helpers.status_code import get_response, generic_error_2
from vendor_app.custom_helpers.model_serializers_helpers import CustomExceptionHandler
from vendor_app.serializers.purchase_serializer import PurchaseOrderRequestDeleteSerailizer, DeletePurchaseOrderResponseSerailizer, \
                            GetPurchaseOrderResponseSerializer, PurchaseOrderGetRequestSerializer, PurchaseOrderRequestSerailizer, \
                            PuchaseOrderReponseCreateUpdateSerializer
from vendor_app.services.purchase_service import get_purchase_service, purchase_create_update_service, delete_purchase_object_service

logger = logging.getLogger("django")


# Purchase Order API
# Here custom api view will not be used it wont work
@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=PurchaseOrderRequestSerailizer,
    responses={"200": PuchaseOrderReponseCreateUpdateSerializer},
    operation_id="Purchase Order Create Update"
)
@api_view(["POST"])
def purchase_order_create_update(request):
    response_obj = None

    try:
        logger.info(request, "request for purchase order update or create")
        response_obj = purchase_create_update_service(request)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in purchase order url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in purchase order url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in purchase order update or create --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


@custom_api_view(
    request_serializer=PurchaseOrderGetRequestSerializer,
    responses={"200": GetPurchaseOrderResponseSerializer},
    operation_id="Get Purchase Order"
)
@csrf_exempt
def get_purchase_order(request):
    response_obj = None

    try:
        logger.info(request, "request for get purchase order")
        response_obj = get_purchase_service(request.validation_serializer.validated_data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in purchase order url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in purchase order url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in get purchase order --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


@csrf_exempt
@custom_api_view(
    request_serializer=PurchaseOrderRequestDeleteSerailizer,
    responses={"200": DeletePurchaseOrderResponseSerailizer},
    operation_id="Delete Purchase Order"
)
def delete_purchase_order(request):
    response_obj = None

    try:
        logger.info(request, "request for purchase order delete")
        response_obj = delete_purchase_object_service(request.validation_serializer.validated_data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in delete purchase url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in delete purchase url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in delete purchase --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)

