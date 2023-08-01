
FROM python:3.9-slim as builder

WORKDIR /app

COPY . /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]