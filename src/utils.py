import uuid
from rest_framework.views import exception_handler

def hex_uuid():
    id = uuid.uuid4()
    return id.hex

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        if type(response.data) is list:
            response.data = {'message': response.data}
        else:
            for error_field in response.data:
                response.data = {'message': response.data[error_field]}
                break

        response.data['status_code'] = response.status_code

    return response