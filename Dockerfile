FROM debian:10.2-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim python3 python3-pip -y
RUN pip3 install --upgrade pip

COPY ./requirements.txt /var/
RUN pip3 install -r /var/requirements.txt

RUN mkdir -p /home/micropub/app
RUN mkdir -p /home/micropub/shared

EXPOSE 8080
WORKDIR /home/micropub/app
ENTRYPOINT ["tail", "-f", "/dev/null"]
