FROM python:3.9.2-alpine3.12 as build

# used by app to determine where the client-side code lives
ENV STATIC_PATH /app/app/static

# install uwsgi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

# install requirements
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9.2-alpine3.12 as base
COPY --from=build /root/.local /root/.local

# (re)installs a few dependencies
RUN apk add pcre-dev hugo

# install source code
COPY ./src .

# load deployment script
COPY ./uwsgi/build-site.sh /usr/local/bin/

############
# Development
#############

FROM base as dev
ENV FLASK_ENV development
ENTRYPOINT ["flask", "run"]

#####
# UAT
#####

FROM base as uat
ENV FLASK_ENV development
ENTRYPOINT ["/root/.local/bin/uwsgi", "--ini", "/etc/uwsgi/micropub.ini"]

############
# Production
############

FROM base as prod
ENV FLASK_ENV production
ENTRYPOINT ["/root/.local/bin/uwsgi", "--ini", "/etc/uwsgi/micropub.ini"]
