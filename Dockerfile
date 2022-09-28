FROM docker.io/library/python:3.10.6-alpine3.15 as build

# used by app to determine where the client-side code lives
ENV STATIC_PATH /app/app/static

# install uwsgi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

# Installs python packages to the users local folder
WORKDIR /app
COPY ./src/requirements.txt /app/
RUN pip install --user -r requirements.txt

FROM docker.io/library/python:3.10.6-alpine3.15 as base
COPY --from=build /root/.local /root/.local

# (re)installs a few dependencies
RUN apk add pcre-dev git openssh

# load deployment script
COPY ./template/build-site.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/build-site.sh

# load uwsgi config
RUN mkdir -p /etc/micropub
COPY ./template/micropub.ini /etc/micropub

# install source code
COPY ./src /app/src

#############
# Development
#############

FROM base as dev

# mount content directories here
RUN mkdir -p /mnt/chaos/content

# mount source code volume here
WORKDIR /mnt/src

ENV FLASK_ENV development
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]

FROM base as test
WORKDIR /app/src
RUN python -m unittest tests.integration

############
# Production
############

FROM test as prod
WORKDIR /app/src
ENV FLASK_ENV production

# adding repo
ENV GIT_SSH_COMMAND "/usr/bin/ssh -i /root/.ssh/micropub_git_rsa"
RUN mkdir -p "/root/.ssh"
COPY ./safe/micropub_git_rsa /root/.ssh
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN git clone --depth 1 git@github.com:acbilson/chaos-content.git /mnt/chaos/content
ENTRYPOINT ["/root/.local/bin/uwsgi", "--ini", "/etc/micropub/micropub.ini"]
