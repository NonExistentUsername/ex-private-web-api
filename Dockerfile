FROM python:3.10.8-alpine3.16

WORKDIR /app

COPY requirements.txt /app

RUN apt install gcc
RUN pip install -r requirements.txt

COPY . .

ENV DEBUG True

EXPOSE 8000

CMD ["uvicorn", "main:app", "--app-dir", "app", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]