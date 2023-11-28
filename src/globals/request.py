from django.conf import settings
from home import models


def RequestExposerMiddleware(get_response):
    def middleware(request):
        models.global_request = request
        response = get_response(request)
        return response
    return middleware
