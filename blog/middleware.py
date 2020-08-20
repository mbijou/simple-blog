from django.utils import translation


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # language_code = 'en'

        # translation.activate(language_code)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
