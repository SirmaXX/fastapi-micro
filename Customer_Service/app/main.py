from fastapi import FastAPI


from .config import DefaultConfig

def create_app():
    app = FastAPI(title="müsteri servisi", description="searchly mülakat servisi") 
    app.config = DefaultConfig
  

    return app