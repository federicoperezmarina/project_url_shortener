# project_url_shortener
This repository is a project to create a url shortener in python using docker and flask. This is my first time using flask and it has been a challenge.

## Table of Contents
* [Docker image](#docker-image)
* [Docker build](#docker-build)
* [Docker run and execute](#docker-run-and-execute)
* [Project description](#project-description)
* [Application in flask](#application-in-flask)
* [Test in flask](#test-in-flask)

## Docker image
First of all we are going to use docker to prepare the environment.
This is the Dockerfile were we can see how to install python, pip and flask. The image base for the project is alpine linux in order to be small, simple and secure. Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox.
```sh
FROM alpine:latest

WORKDIR /python-docker-url-shortener
COPY . .

RUN apk add python3 && \
    apk add py3-pip && \
    apk --no-cache add curl && \
    pip3 install flask && \
    pip3 install flask-jsonpify && \
    pip3 install flask-restful && \
    pip3 install shortuuid && \
    pip3 install pytest && \
    pip3 install validators

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
docker run -it -p 5000:5000 python-docker-url-shortener /bin/sh
```

In this step we can execute the application inside the container:
```sh
python3 application.py 
```

In the output, we can see that the application is running
```sh
 * Serving Flask app 'application' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 370-421-007
```

We will have to open a new tab in order to execute the api rest endpoints, but before we are going to introduce the concept of a good practices in the life cycle of an app development.

## Project description
The project consist in create an url shortener with the flask python framework. We have to take in consideration 5 topics with the next development. We have to ensure that a good application has:
    - Security: validate the input data
    - Quality: having test
    - Performance: the application don't have bottleneck
    - Analytics: to measure how the application is working
    - Observability: to monitor infraestructure, checking microservices, logging errors


## Application in flask
We have here the code developed for the url shortener:
```python
from flask import Flask, request, redirect, Response
from flask_restful import Resource, Api
from validators import url
from shortuuid import ShortUUID

# init Flask framework
app = Flask(__name__)
api = Api(app)

# our shortened urls (fake database or in memory :) )
urls_shortened = {}

# method GET to obtain all urls shortened
class Urls(Resource):
    def get(self):
        return urls_shortened

# method PUT to shorten an url
class UrlShortener(Resource):
    def put(self):
        # using shortuuid package provides close to 0 risk collision
        url_id = ShortUUID().random(length=8).lower()

        # validating correct url, secure
        if url(request.form['data']): 
            urls_shortened[url_id] = request.form['data']
            result = {
                "url_id" : url_id,
                "url" : urls_shortened[url_id]
            }
            return result

        # Not valid url
        return Response("message: 'Not valid url'\n",status=400)

# method GET to redirect a shortened url
class UrlRedirect(Resource):
    def get(self, url_id):
        return redirect(urls_shortened[url_id], code=302)

# routing
api.add_resource(Urls, '/all')
api.add_resource(UrlRedirect, '/<string:url_id>')
api.add_resource(UrlShortener, '/')

if __name__ == '__main__':
    app.run(debug=True)
```

In order to execute the api rest enpoints in the docker we should execute some commands in a new tab:
```sh
docker ps | grep 'python-docker-url-shortener' | awk '{ print $1 }' > container_id.out

docker exec -it $(cat container_id.out) /bin/sh

ls -lha
```

The output is something like this:
```sh
drwxr-xr-x    1 root     root        4.0K Jul 26 21:43 .
drwxr-xr-x    1 root     root        4.0K Jul 26 21:44 ..
drwxr-xr-x    7 root     root        4.0K Jul 26 21:38 .git
-rw-r--r--    1 root     root          25 Jul 26 00:26 .gitignore
drwxr-xr-x    3 root     root        4.0K Jul 26 21:38 .pytest_cache
-rw-r--r--    1 root     root         370 Jul 26 21:42 Dockerfile
-rw-r--r--    1 root     root        3.4K Jul 26 21:41 README.md
drwxr-xr-x    2 root     root        4.0K Jul 26 21:38 __pycache__
-rw-r--r--    1 root     root        1.3K Jul 26 00:09 application.py
-rw-r--r--    1 root     root         919 Jul 26 00:35 test.py
```

Now we are able to execute the application:
```sh
command to list all tiny urls:
curl http://localhost:5000/all

output:
{}

command to shorten an url:
curl http://localhost:5000/ -d "data=http://www.marca.com" -X PUT

output:
{
    "url_id": "jwpkt7ph",
    "url": "http://www.marca.com"
}

command to list all tiny urls:
curl http://localhost:5000/all

output:
{
    "jwpkt7ph": "http://www.marca.com"
}

command to see the redirect of an url:
curl http://localhost:5000/jwpkt7ph

output:
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="http://www.marca.com">http://www.marca.com</a>. If not, click the link.
```

## Test in flask
Now we are going to see the test that validate our develop code:
```python
import pytest
import json
from application import app

def test_urls():
    with app.test_client() as client:
 
        response = client.get("/all")
        assert response.status_code == 200
        response_json = json.loads(response.data)
        assert not response_json

        client.put("/", data={"data":"http://www.testurl.com"})

        response = client.get("/all")
        assert response.status_code == 200
        response_json = json.loads(response.data)
        assert len ( response_json ) == 1


def test_url_shortener():
    with app.test_client() as client:
 
        response = client.put("/", data={"data":"http://www.testurl.com"})
        response_json = json.loads(response.data)
        assert response.status_code == 200
        response_2 = client.get("/"+response_json['url_id'])
        assert response_2.status_code == 302


def test_url_shortener_400():
    with app.test_client() as client:
 
        response = client.put("/", data={"data":""})
        assert response.status_code == 400
```

We are testing all the urls that we have shown before and the different responses like 200, 400 or 302. To execute it we have to do:
```sh
pytest test.py 
```

Output:
```sh
================================== test session starts ===================================
platform linux -- Python 3.9.13, pytest-7.1.2, pluggy-1.0.0
rootdir: /python-docker-url-shortener
collected 3 items                                                                        

test.py ...                                                                        [100%]

=================================== 3 passed in 0.26s ====================================
```
