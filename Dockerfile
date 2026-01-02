FROM python:3.12-slim 

WORKDIR /app 

RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \ 
  && rm -rf /var/lib/apt/lists/* 


COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

# RUN python manage.py collectstatic --noinput 


RUN useradd -m appuser 
USER appuser

EXPOSE 8080 

CMD ["uvicorn", "easymart.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
