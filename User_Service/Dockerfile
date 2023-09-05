FROM python:3.9
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "--reload-dir", "/app", "app.main:app", "--port", "5001"]