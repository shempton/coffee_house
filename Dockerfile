FROM python:3.11.2-buster

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt --no-cache-dir

RUN python manage.py migrate

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]