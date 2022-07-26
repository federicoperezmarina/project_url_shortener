import pytest
import json
from application import app

def test_urls():
	# Create a test client using the Flask application configured for testing
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
	# Create a test client using the Flask application configured for testing
	with app.test_client() as client:
 
		response = client.put("/", data={"data":"http://www.testurl.com"})
		response_json = json.loads(response.data)
		assert response.status_code == 200
		response_2 = client.get("/"+response_json['url_id'])
		assert response_2.status_code == 302
