FROM alpine:latest

RUN apk add --no-cache python3 curl && \
  python3 -m ensurepip && \
  pip3 install flask apscheduler

# Mount code volume from host to run in container
CMD [ "python3", "/code/run_server.py" ]
