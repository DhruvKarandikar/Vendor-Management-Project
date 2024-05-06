from django.urls import path
from vendor_app.views import *

urlpatterns = [

    # paths for vendor

    path('vendor_app/vendor', vendor_create_update, name='vendor_crud'),
    path('vendor_app/vendor_get', get_vendor, name='vendor_get'),
    path('vendor_app/vendor_delete', delete_vendor, name='vendor_delete'),
    path('vendor_app/vendor_performance', get_vendor_performance, name='vendor_performance'),

    path('purchase/purchase_order', purchase_order_create_update, name='purchase_crud'),
    path('purchase/get_purchase_order', get_purchase_order, name='purchase_order_get'),
    path('purchase/delete_purchase_order', delete_purchase_order, name='vendor_delete'),

    

]