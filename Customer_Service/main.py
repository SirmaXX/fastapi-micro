from fastapi import FastAPI
from app.main import create_app
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")