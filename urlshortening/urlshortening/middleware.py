import logging
import datetime

logging.basicConfig(level=10)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(
            f"[{request.method}]:: [{request.get_full_path()}] :: {datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
        )
        response = self.get_response(request)
        return response
