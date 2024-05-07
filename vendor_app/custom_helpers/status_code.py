from vendor_app.custom_helpers.consts import *


success = {STATUS_CODE: SUCCESS_CODE, MESSAGE: "Success"}

def invalid_log_model(table_name):
    return {
        STATUS_CODE: 2100001,
        MESSAGE: f'Invalid log model initialized for model {table_name}',
    }

generic_error_1 = {STATUS_CODE: int(f"2110000"), MESSAGE: "Invalid request details"}
generic_error_2 = {STATUS_CODE: int(f"2110001"), MESSAGE: "Please try again after sometime"}

# Error Code invalid
search_obj_invalid = {STATUS_CODE: 2110010, MESSAGE: "Please enter the object within the list field"}
invalid_request_pass_id = {STATUS_CODE: 2110011, MESSAGE: "ID is mandatory"}
no_object_exist = {STATUS_CODE: 2110012, MESSAGE: "Object does not exists kindly enter valid Id"}
invalid_request_purchase_order = {STATUS_CODE: 2110013, MESSAGE: "Please vendor id for accurate results not Id"}
invalid_request_vendor_id = {STATUS_CODE: 2110014, MESSAGE: "Pass Id when list object is 'Single'"}

def get_response(status_attribute, data=None):
    if data is None:
        return {'status': status_attribute['status_code'], 'message': status_attribute['message']}
    else:
        return {'status': status_attribute['status_code'], 'message': status_attribute['message'], 'data': data}


def log_info_message(request, message = "Info"):
    return (f"{message} --> {request.body}")
