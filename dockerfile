FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & celery -A gincana.celery worker --pool=solo -l info & celery -A gincana beat -l INFO"]