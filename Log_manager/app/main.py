from fastapi import FastAPI, Request,Response
from time import gmtime, strftime
from app.routes.log import log
from app.routes.webapplog import applog



def create_app():
    app = FastAPI(title="log servisi", description="mongoya bağlı log servisi")
    app.include_router(log)
    app.include_router(applog)
 

    return app