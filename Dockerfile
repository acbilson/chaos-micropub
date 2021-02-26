FROM python:alpine as develop

COPY ./app/flask-dance/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY ./app/flask-dance/ .

EXPOSE 8080

ENTRYPOINT ["flask", "run"]
