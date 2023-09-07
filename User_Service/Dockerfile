FROM python:3.9
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["python3", "main.py"]