set dotenv-load

# builds a development docker image.
build:
  COMMIT_ID=$(git rev-parse --short HEAD); \
  docker build \
  --target dev \
  -t acbilson/micropub:latest \
  -t acbilson/micropub:${COMMIT_ID} .

# starts a development docker image.
start:
  docker run --rm \
  --expose ${EXPOSED_PORT} -p ${EXPOSED_PORT}:80 \
  -e "SITE=http://localhost:${EXPOSED_PORT}" \
  -e "CLIENT_ID=${GITHUB_CLIENT_ID}" \
  -e "CLIENT_SECRET=${GITHUB_CLIENT_SECRET}" \
  -e "FLASK_SECRET_KEY=${FLASK_SECRET_KEY}" \
  -e "SESSION_SECRET=${SESSION_SECRET}" \
  -e "CONTENT_PATH=/mnt/chaos/content" \
  -v ${SOURCE_PATH}/src:/mnt/src \
  -v ${SOURCE_PATH}/content:/mnt/chaos/content \
  --name micropub \
  acbilson/micropub:latest
