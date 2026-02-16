from __future__ import annotations
import time
import uuid
from inventory.logging.get_logger import get_configured_logger

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = get_configured_logger()   # process lifetime

    def __call__(self, request):
        request_id = str(uuid.uuid4())          # request lifetime
        request.request_id = request_id
        start = time.perf_counter()

        self.logger.info(
            "request_received",
            extra={
                "event": "request_received",
                "request_id": request_id,
                "method": request.method,
                "path": request.path,
            },
        )

        try:
            response = self.get_response(request)
        except Exception:
            self.logger.exception(
                "request_failed",
                extra={
                    "event": "request_failed",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.path,
                },
            )
            raise
        latency_ms = (time.perf_counter() - start) * 1000.0

        self.logger.info(
            "request_completed",
            extra={
                "event": "request_completed",
                "request_id": request_id,
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "latency_ms": latency_ms,
            },
        )

        return response
