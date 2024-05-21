import logging
import datetime

logging.basicConfig(level=10)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        logging.info(f"[{request.method}]:: [{request.get_full_path()}] :: {datetime.datetime.now().strftime("%Y-%m-%dT%h:%M:%S")}")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response