from rest_framework import serializers
from django.db.models import Q
from vendor_app.models import *
from django.db.transaction import atomic
from vendor_app.custom_helpers.model_serializers_helpers import dict_get_key_from_value, help_text_for_dict, get_datetime_to_str, \
            common_checking_and_passing_value_from_list_dict, CustomExceptionHandler, comman_create_update_services, number_to_decimal
from vendor_app.custom_helpers.consts import *
from vendor_app.custom_helpers.status_code import *


class HeadPurchaseOrderSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    vendor_id = serializers.IntegerField(required=True)
    po_number = serializers.CharField(required=True)
    order_date = serializers.DateTimeField(required=True)
    delivery_date = serializers.DateTimeField(required=True)
    items = serializers.JSONField(required=True)
    quantity = serializers.IntegerField(required=False)
    current_status = serializers.IntegerField(required=False, help_text=help_text_for_dict(current_status_po))
    quality_rating = serializers.IntegerField(required=False)
    issue_date = serializers.DateTimeField(required=False)
    acknowledgment_date = serializers.DateTimeField(required=False)

    class Meta:
        model = PurchaseOrder
        exclude = ("status", "creation_date", "creation_by", "updation_date", "updation_by",)
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}

    
    def to_representation(self, data):
        data = super().to_representation(data)

        if data.get('order_date'):
            data['order_date'] = get_datetime_to_str(data['order_date'], DATE_YYYY_MM_DD)
        
        if data.get('delivery_date'):
            data['delivery_date'] = get_datetime_to_str(data['delivery_date'], DATE_YYYY_MM_DD)
            
        if data['issue_date']:
            data['issue_date'] = get_datetime_to_str(data['issue_date'], DATE_YYYY_MM_DD)
        
        if data['acknowledgment_date']:
            data['acknowledgment_date'] = get_datetime_to_str(data['acknowledgment_date'], DATE_YYYY_MM_DD)
        
        if data['current_status']:    
            data['current_status'] = dict_get_key_from_value(current_status_po, data['current_status'])
        
        if data.get('quality_rating'):
            data["quality_rating"] = number_to_decimal(data["quality_rating"])
        
        return data

    @atomic
    def create(self, validated_data):
        return (validated_data)

    @atomic
    def update(self, instance, validated_data):
        return (instance, validated_data)

class PurchaseOrderRequestSerailizer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    vendor_id = serializers.IntegerField(required=False)
    po_number = serializers.CharField(required=False)
    order_date = serializers.DateTimeField(required=False)
    delivery_date = serializers.DateTimeField(required=False)
    items = serializers.JSONField(required=False)
    quantity = serializers.IntegerField(required=False)
    current_status = serializers.CharField(required=False, help_text=help_text_for_dict(current_status_po))
    quality_rating = serializers.FloatField(required=False)
    issue_date = serializers.DateTimeField(required=False)
    acknowledgment_date = serializers.DateTimeField(required=False)

    class Meta:
        model = PurchaseOrder
        exclude = ("status", "creation_date", "creation_by", "updation_date", "updation_by",)

    def validate_current_status(self, value):
        return common_checking_and_passing_value_from_list_dict(value, current_status_po, invalid_request_current_status)

    def validate_quality_rating(self, value):
        if value != None and value != "":
            value = value * 100
        return value

    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}
    
    def to_representation(self, data):
        data = super().to_representation(data)
        
        if data.get('order_date'):
            data['order_date'] = get_datetime_to_str(data['order_date'], DATE_YYYY_MM_DD)
        
        if data.get('delivery_date'):
            data['delivery_date'] = get_datetime_to_str(data['delivery_date'], DATE_YYYY_MM_DD)
            
        if data['issue_date']:
            data['issue_date'] = get_datetime_to_str(data['issue_date'], DATE_YYYY_MM_DD)
        
        if data['acknowledgment_date']:
            data['acknowledgment_date'] = get_datetime_to_str(data['acknowledgment_date'], DATE_YYYY_MM_DD)

        if data.get('quality_rating'):
            data["quality_rating"] = number_to_decimal(data["quality_rating"])

        if data.get('current_status'):
            data['current_status'] = dict_get_key_from_value(current_status_po, data['current_status'])

        return data
    
    @atomic
    def create(self, validated_data):
        return comman_create_update_services(self, validated_data)

    @atomic
    def update(self, instance, validated_data):
        return comman_create_update_services(self, validated_data, instance)

class PuchaseOrderReponseCreateUpdateSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = HeadPurchaseOrderSerializer(required=False)

    class Meta:
        model = PurchaseOrder
        fields = ("status", "message", "data", )


# Purchase Order Get Serializer request response
class PurchaseOrderGetRequestSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    vendor_id = serializers.IntegerField(required=False)
    search_object = serializers.CharField(required=True, help_text=search_by_object)

    class Meta:
        model = PurchaseOrder
        fields = ("id", "search_object", "vendor_id",)

    def validate(self, data):

        data = super().validate(data)

        id = data.get('id', None)
        vendor_id = data.get('vendor_id', None)
        search_by_object = data.get('search_object')

        if search_by_object == 'single' and not id and vendor_id:
            raise CustomExceptionHandler(invalid_request_pass_id)
        
        if search_by_object == 'single' and not id:
            raise CustomExceptionHandler(invalid_request_pass_id)
        
        if search_by_object == 'single' and vendor_id:
            raise CustomExceptionHandler(invalid_request_vendor_id)
        
        if search_by_object == 'all' and vendor_id and id:
            raise CustomExceptionHandler(invalid_request_purchase_order)

        if search_by_object == 'all' and (vendor_id or id):
            raise CustomExceptionHandler(invalid_request_for_all)

        return data


class GetPurchaseOrderResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = HeadPurchaseOrderSerializer(many=True, required=False)

    class Meta:
        model = PurchaseOrder
        fields = ("status", "message", "data", )


# Purchase Order Delete Serializer request response

class PurchaseOrderRequestDeleteSerailizer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=True)

    class Meta:
        model = PurchaseOrder
        fields = ("id",)


class DeletePurchaseOrderResponseSerailizer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)

