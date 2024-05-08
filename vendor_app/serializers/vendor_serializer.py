from rest_framework import serializers
from django.db.models import Q
from vendor_app.models import *
from django.db.transaction import atomic
from vendor_app.custom_helpers.model_serializers_helpers import dict_get_key_from_value, help_text_for_dict, get_datetime_to_str, \
            common_checking_and_passing_value_from_list_dict, comman_create_update_services
from vendor_app.custom_helpers.consts import *
from vendor_app.custom_helpers.status_code import *

class HeadVendorPerformanceSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    vendor_id = serializers.IntegerField(required=False)
    date =  serializers.DateTimeField(required=False)
    on_time_delivery_rate =  serializers.FloatField(required=False)
    quality_rating_avg = serializers.FloatField(required=False)
    average_response_time = serializers.FloatField(required=False)
    fulfillment_rate = serializers.FloatField(required=False)

    class Meta:
        model = VendorPerformance
        exclude = ("status", "creation_date", "creation_by", "updation_date", "updation_by",)
    
    def validate_on_time_delivery_rate(self, value):
        if value != None and value != "":
            value = value * 100
        return value
    
    def validate_average_response_time(self, value):
        if value != None and value != "":
            value = value * 100
        return value

    def validate_quality_rating_avg(self, value):
        if value != None and value != "":
            value = value * 100
        return value
    
    def validate_fulfillment_rate(self, value):
        if value != None and value != "":
            value = value * 100
        return value
    
    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}


class HeadVendorDetailSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    vendor_name = serializers.CharField(required=False)
    contact_details = serializers.CharField(required=False)
    vendor_code = serializers.UUIDField(required=False)
    on_time_delivery_rate = serializers.FloatField(required=False)
    quality_rating_avg = serializers.FloatField(required=False)
    average_response_time = serializers.FloatField(required=False)
    fulfillment_rate = serializers.FloatField(required=False)

    class Meta:
        model = VendorDetail
        fields = ('id','vendor_name', 'contact_details', 'vendor_code', 'on_time_delivery_rate', 
                  'quality_rating_avg', 'average_response_time', 'fulfillment_rate',)

    #TODO add * 100 to positive integer field here and pass it further in internal value
    def validate_on_time_delivery_rate(self, value):
        if value != None and value != "":
            value = value * 100
        return value
    
    def validate_average_response_time(self, value):
        if value != None and value != "":
            value = value * 100
        return value

    def validate_quality_rating_avg(self, value):
        if value != None and value != "":
            value = value * 100
        return value
    
    def validate_fulfillment_rate(self, value):
        if value != None and value != "":
            value = value * 100
        return value

    def to_representation(self, data):
        data = super().to_representation(data)

        # data['on_time_delivery_rate'] = 
        # data['quality_rating_avg'] = 
        # data['average_response_time'] = 
        # data['fulfillment_rate'] = 
        return data
    
    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}



# vendnor detail Crud serializer
class VendorDetailCreateUpdateSerializer(HeadVendorDetailSerializer):

    # from .purchase_serializer import HeadPurchaseOrderSerializer

    vendor_performances = HeadVendorPerformanceSerializer(many=True,required=False)
    # vendor_purchase_order = HeadPurchaseOrderSerializer(many=True, source='vendor_purchase_orders',required=False)

    class Meta:
        model = VendorDetail
        fields = ('id','vendor_name', 'contact_details', 'vendor_code', 'on_time_delivery_rate', 
                  'quality_rating_avg', 'average_response_time', 'fulfillment_rate','vendor_performances',)

    def to_representation(self, data):
        data = super().to_representation(data)

        vendor_id = data.get('id')
        vendor_performance_obj = VendorPerformance.objects.filter(vendor_id=vendor_id)
        vendor_performance_serializer = HeadVendorPerformanceSerializer(vendor_performance_obj, many=True)
        data['vendor_performances'] = vendor_performance_serializer.data
        return data

    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}

    
    @atomic
    def create(self, validated_data):
        return comman_create_update_services(self, validated_data)

    @atomic
    def update(self, instance, validated_data):
        return comman_create_update_services(self, validated_data, instance)


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
    search_object = serializers.CharField(required=True, help_text=search_by_object)

    class Meta:
        model = VendorDetail
        fields = ("id", "search_object",)




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
