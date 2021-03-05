FROM python:alpine as build

WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
RUN mkdir -p /home/comments
COPY ./scripts/git-deploy.sh /usr/bin/

FROM build as develop
ENV OAUTHLIB_INSECURE_TRANSPORT 1
ENV FLASK_APP main
EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
