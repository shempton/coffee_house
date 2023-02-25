FROM python:3.11.2-buster

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

#  docker build . -t django:v1
#  docker run -it -p 8000:8000 django:v1