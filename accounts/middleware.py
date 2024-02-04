from django.contrib.auth import get_user

class HtmxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = get_user(request)
        if user.is_authenticated and 'HX-Request' in request.headers and response.status_code == 302:
            response.status_code = 204
            response['HX-Redirect'] = '/'  # change this to your home page URL
        return response