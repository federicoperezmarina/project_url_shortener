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