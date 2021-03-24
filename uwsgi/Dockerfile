FROM python:3.9.2-alpine3.12

# used by app to determine where the client-side code lives
ENV STATIC_PATH /app/app/static

# install uwsgi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

# install requirements
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .

# remove build dependencies
RUN apk del python3-dev build-base linux-headers

# load deployment script
COPY ./uwsgi/build-site.sh /usr/local/bin/

# load uwsgi configuration
COPY ./uwsgi/micropub.ini /etc/uwsgi/

EXPOSE 5000
ENTRYPOINT ["uwsgi", "--ini", "/etc/uwsgi/micropub.ini"]
