FROM python:3.9.2-alpine

# used by app to determine where the client-side code lives
ENV STATIC_PATH /app/app/static

# update environtment
RUN apk update && apk upgrade
RUN pip install --upgrade pip

# install uwsgi dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev

# install requirements
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .

# create path for new comments
RUN mkdir -p /home/comments

# load deployment script
COPY ./scripts/git-deploy.sh /usr/bin/

# load uwsgi script
COPY ./uwsgi/micropub.ini /etc/uwsgi/

EXPOSE 5000
ENTRYPOINT ["uwsgi", "--ini", "/etc/uwsgi/micropub.ini"]
