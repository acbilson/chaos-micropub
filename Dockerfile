FROM debian:buster-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim python3 python3-pip -y

COPY ./requirements.txt /var/
RUN pip3 install -r /var/requirements.txt

RUN mkdir -p /home/micropub/app

EXPOSE 8080
WORKDIR /home/micropub/app
ENTRYPOINT ["python3", "wsgi.py"]
