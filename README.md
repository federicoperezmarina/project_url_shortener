# project_url_shortener
This repository is a project to create a url shortener in python using docker and flask

## Table of Contents
* [Docker image](#docker-image)
* [Docker build](#docker-build)
* [Docker run and execute](#docker-run-and-execute)

## Docker image
First of all we are going to use docker to prepare the environment.
edirect("http://www.example.com", code=302)
This is the Dockerfile were we can see how to install python, pip and flask. The image base for the project is alpine linux in order to be small, simple and secure. Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox.
```sh
FROM alpine:latest

WORKDIR /python-docker-url-shortener
COPY . .

RUN apk add python3 && \
    apk add py3-pip && \
    pip3 install flask && \
    pip3 install flask-jsonpify && \
    pip3 install flask-restful && \
    pip3 install shortuuid && \
    pip3 install pytest

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```


## Docker build
We need to create the docker image in order to launch / execute the code. This is the way to create the docker image
```sh
docker build --tag python-docker-url-shortener .
```


## Docker run and execute
Now we are able to use the image with the next command
```sh
docker run -it -p 5000:5000 python-docker-url-shortener
```