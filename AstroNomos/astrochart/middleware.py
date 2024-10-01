# astrochart/middleware.py

class AllowIframeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/__/auth/iframe'):
            response['X-Frame-Options'] = 'ALLOWALL'
        return response
