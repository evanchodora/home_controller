FROM node:alpine
WORKDIR /usr/src/app
RUN apk add --update git && \
  rm -rf /tmp/* /var/cache/apk/*
COPY . /usr/src/app
RUN npm install
EXPOSE 5005
ENTRYPOINT ["node", "castWebApi.js", "--hostname=0.0.0.0", "--port=5005"]
