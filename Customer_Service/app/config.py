import os

class DefaultConfig:
    DEBUG = True
    SECRET_KEY = "your-secret-key"
    DATABASE_URI = os.environ.get('DATABASE_URL')