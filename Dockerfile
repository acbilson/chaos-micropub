FROM debian:buster-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim python3 python3-pip -y

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir -p /home/micropub/app

EXPOSE 8080
ENTRYPOINT ["python3", "wsgi.py"]
