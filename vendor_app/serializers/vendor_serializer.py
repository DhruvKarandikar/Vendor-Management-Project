from rest_framework import serializers
from django.db.models import Q
from vendor_app.models import *
from django.db.transaction import atomic
from vendor_app.services.vendor_service import vendor_create_update_service_serializer
from vendor_app.custom_helpers.model_serializers_helpers import dict_get_key_from_value, help_text_for_dict, get_datetime_to_str, \
            common_checking_and_passing_value_from_list_dict
from vendor_app.custom_helpers.consts import *
from vendor_app.custom_helpers.status_code import *

class HeadVendorPerformanceSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    vendor_id = serializers.IntegerField(required=False)
    date =  serializers.DateTimeField(required=False)
    on_time_delivery_rate =  serializers.IntegerField(required=False)
    quality_rating_avg = serializers.IntegerField(required=False)
    average_response_time = serializers.IntegerField(required=False)
    fulfillment_rate = serializers.IntegerField(required=False)

    class Meta:
        model = VendorPerformance
        exclude = ("status", "creation_date", "creation_by", "updation_date", "updation_by",)

class HeadVendorDetailSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    vendor_name = serializers.CharField(required=False)
    contact_details = serializers.CharField(required=False)
    vendor_code = serializers.UUIDField(required=False)
    on_time_delivery_rate = serializers.IntegerField(required=False)
    quality_rating_avg = serializers.IntegerField(required=False)
    average_response_time = serializers.IntegerField(required=False)
    fulfillment_rate = serializers.IntegerField(required=False)

    class Meta:
        model = VendorDetail
        exclude = ("status", "creation_date", "creation_by", "updation_date", "updation_by",)

    #TODO add * 100 to positive integer field here and pass it further in internal value
    def validate_on_time_delivery_rate(self, value):
        if value != None and value != "":
            value = value * 100
        return value


    def to_representation(self, data):
        data = super(HeadVendorDetailSerializer).to_representation(data)
        return data

    @atomic
    def create(self, validated_data):
        return vendor_create_update_service_serializer(validated_data)

    @atomic
    def update(self, instance, validated_data):
        return vendor_create_update_service_serializer(instance, validated_data)


# vendnor detail Crud serializer
class VendorDetailCreateUpdateSerializer(HeadVendorDetailSerializer):

    vendor_performance = HeadVendorPerformanceSerializer(many=True, required=False)

    class Meta:
        model = VendorDetail
        exclude = ("status", "creation_date", "creation_by", "updation_date", "updation_by",)


class VendorDetailCrudResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = HeadVendorDetailSerializer(required=False)

    class Meta:
        model = PurchaseOrder
        fields = ("status", "message", "data", )


# Get Vendor Serializer

class GetVendorDetailRequestSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    search_object = serializers.ListField(required=True, help_text=search_by_object)

    class Meta:
        model = VendorDetail
        fields = ("id", "search_object",)
    
    def validate_search_object(self, value):
        if value:
            for val in value:
                common_checking_and_passing_value_from_list_dict(val, search_by_object, search_obj_invalid)
            return value



class GetVendorDetailResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = HeadVendorDetailSerializer(many=True, required=False)

    class Meta:
        model = PurchaseOrder
        fields = ("status", "message", "data", )


# Delete Vendor Detail

class VendorDetailRequestDeleteSerailizer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=True)

    class Meta:
        model = VendorDetail
        fields = ("id",)


class DeleteVendorDetailResponseSerailizer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)


# Get Vendor Performance

class GetVendorPerformanceRequestSerailizer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=True)

    class Meta:
        model = VendorPerformance
        fields = ("id",)

class GetVendorPerformanceResponseSerailizer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = HeadVendorPerformanceSerializer(required=False)
