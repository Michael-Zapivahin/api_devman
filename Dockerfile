
FROM python:3.9-slim as builder
WORKDIR /app
COPY . /app
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/

CMD ["python", "main.py"]