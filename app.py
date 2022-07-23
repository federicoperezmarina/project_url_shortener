from flask import Flask, request
from flask_restful import Resource, Api
import random
import string

app = Flask(__name__)
api = Api(app)

urls_shortened = {}

class Urls(Resource):
    def get(self):
        return urls_shortened

class UrlShortener(Resource):
    def put(self):
        url_id = ''.join(random.choice(string.ascii_uppercase) for i in range(8))
        urls_shortened[url_id] = request.form['data']
        return {url_id: urls_shortened[url_id]}

class UrlsRedirect(Resource):
    def get(self, url_id):
        return urls_shortened[url_id]

api.add_resource(Urls, '/all')
api.add_resource(UrlsRedirect, '/<string:url_id>')
api.add_resource(UrlShortener, '/')

if __name__ == '__main__':
    app.run(debug=True)