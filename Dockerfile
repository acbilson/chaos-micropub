FROM python:3.9.2-alpine3.12 as build

# used by app to determine where the client-side code lives
ENV STATIC_PATH /app/app/static

# install uwsgi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

# install requirements
WORKDIR /app
COPY ./src/requirements.txt /app/
RUN pip install --user -r requirements.txt

FROM python:3.9.2-alpine3.12 as base
COPY --from=build /root/.local /root/.local

# (re)installs a few dependencies
RUN apk add pcre-dev hugo

# install source code
COPY ./src /app/src

# load deployment script
COPY ./dist/build-site.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/build-site.sh

# load hugo config
RUN mkdir -p /etc/hugo
COPY ./dist/config.toml /etc/hugo/

# load uwsgi config
RUN mkdir -p /etc/micropub
COPY ./dist/micropub.ini /etc/micropub

#############
# Development
#############

FROM base as dev

# mounts source code volume here
WORKDIR /mnt/src

ENV FLASK_ENV development
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]

#####
# UAT
#####

FROM base as uat
ENV FLASK_ENV production
ENTRYPOINT ["/root/.local/bin/uwsgi", "--ini", "/etc/micropub/micropub.ini"]

############
# Production
############

FROM base as prod
ENV FLASK_ENV production
ENTRYPOINT ["/root/.local/bin/uwsgi", "--ini", "/etc/micropub/micropub.ini"]
