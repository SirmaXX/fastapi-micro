
from fastapi import FastAPI
import starlette.status as status
import urllib,json,requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse,RedirectResponse

from typing import Optional,List
from app.Routers.restapi import restapiroute
from app.Controller.Api_User_Controller import Api_User_Controller
from app.Lib.common import paginate,pagecount
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address




def create_app():
  limiter = Limiter(key_func=get_remote_address)
  app = FastAPI(title="apigateway", description="apigateway")
  app.state.limiter = limiter
  app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
  app.include_router(restapiroute, prefix="/v1/api")
  return app

