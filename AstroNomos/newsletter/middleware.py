from django.http import HttpResponsePermanentRedirect

class RedirectToWwwMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == 'astro-nomos.com':
            return HttpResponsePermanentRedirect(f'http://www.astro-nomos.com{request.path}')
        return self.get_response(request)