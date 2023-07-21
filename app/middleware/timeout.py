import asyncio
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware


class TimeoutMiddleware(BaseHTTPMiddleware):
  """
  Return gateway timeout error (504)
  if the request processing time is above a certain threshold
  """

  def __init__(self, app: ASGIApp, timeout: int = 10):
    super().__init__(app)
    self.timeout = int(timeout)

  async def dispatch(self, request: Request, call_next: Callable) -> Response:
    try:
      return await asyncio.wait_for(call_next(request), timeout=self.timeout)
    except asyncio.TimeoutError:     
      print("Request timeout.") 
      return JSONResponse(
        content={ "status": status.HTTP_504_GATEWAY_TIMEOUT, "message": "Request timeout." },
        status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )
      