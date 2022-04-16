from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import exceptions, status
from rest_framework.views import set_rollback
from rest_framework.response import Response


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
        
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
            
        print (exc)
        if isinstance(exc.detail, (list, dict)):

            if context["request"].stream.path == "/api/auth/users/resend_activation_with_sms/":
                data = {
                    "code":"number_is_invalid",
                    "detail":"Phone number must be entered in the format: '09999999999'. Up to 11 digits allowed."
                }
            else:
                data = exc.get_full_details()

            
        else:
            data = exc.get_full_details()

        set_rollback()

        return Response(data, status=exc.status_code, headers=headers)
    else :
        return None
