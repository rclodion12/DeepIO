FROM nikolaik/python-nodejs:python3.6-nodejs13

# set working directory
WORKDIR /app

COPY . .

RUN apt-get update \
 && apt-get install -y r-base python3-venv python3-pip \
 && apt-get update \
 && npm install

# start app
CMD ["npm", "start"]

