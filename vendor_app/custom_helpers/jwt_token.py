from vendor_app.custom_helpers.consts import *
import jwt
import uuid
import threading

request_local = threading.local()


def get_request():
    return getattr(request_local, 'request', None)


class CustomMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #  After request the code will go here
        authorization = request.headers.get("Authorization")

        http_request_id = request.headers[HTTP_REQUEST_ID] if HTTP_REQUEST_ID in request.headers else str(uuid.uuid4())
        request.META[HTTP_REQUEST_ID] = http_request_id

        token = authorization.split(" ")[1] if authorization else authorization
        if token:
            decoded = jwt.decode(token, options={"verify_signature": False})
            import pdb
            pdb.set_trace()
            request.user_id = CREATION_BY
            request.user_name = DEFAULT_ROLE
        else:
            request.user_id = CREATION_BY
            request.user_name = DEFAULT_ROLE

        request_local.request = request
        
        response = self.get_response(request)
        response.headers[HTTP_REQUEST_ID] = http_request_id

        return response
