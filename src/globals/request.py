from django.conf import settings
from . import functions


def RequestExposerMiddleware(get_response):
    def middleware(request):
        functions.global_request = request
        response = get_response(request)
        return response
    return middleware
