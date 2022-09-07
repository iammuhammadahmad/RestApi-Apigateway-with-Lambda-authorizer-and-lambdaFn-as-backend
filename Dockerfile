FROM node:lts-alpine

ENV SOURCE_DIR=/

COPY . $SOURCE_DIR
WORKDIR $SOURCE_DIR

RUN npm install -g npm@8.19.1
RUN apk --no-cache add python3 py3-pip
RUN npm i -g aws-cdk
RUN cdk --version
RUN pip3 --version
RUN pip3 install -r requirements.txt