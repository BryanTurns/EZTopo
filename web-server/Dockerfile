FROM node:18-alpine

RUN mkdir /app 

WORKDIR /app

COPY package.json /app
COPY tailwind.config.js /app
RUN npm install

COPY public/ /app/public
COPY src/ /app/src

CMD [ "npm", "start" ]