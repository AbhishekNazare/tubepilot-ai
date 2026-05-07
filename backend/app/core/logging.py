import json
import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logging.info(
        json.dumps(
            {
                "event": "request",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }
        )
    )
    return response

