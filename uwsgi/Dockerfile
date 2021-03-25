FROM python:3.9.2-alpine3.12 as build

# used by app to determine where the client-side code lives
ENV STATIC_PATH /app/app/static

# install uwsgi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

# install requirements
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9.2-alpine3.12 as run
COPY --from=build /root/.local /root/.local

# reinstalls a few dependencies
RUN apk add pcre-dev

# install source code
COPY ./src .

# load deployment script
COPY ./uwsgi/build-site.sh /usr/local/bin/

# load uwsgi configuration
COPY ./uwsgi/micropub.ini /etc/uwsgi/

EXPOSE 5000
ENTRYPOINT ["/root/.local/bin/uwsgi", "--ini", "/etc/uwsgi/micropub.ini"]
