FROM alpine:latest

WORKDIR /python-docker-url-shortener
COPY . .

RUN apk add python3 && \
    apk add py3-pip && \    
    pip3 install flask && \ 
    pip3 install flask-jsonpify && \
    pip3 install flask-restful

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]