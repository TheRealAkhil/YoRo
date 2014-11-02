from datetime import datetime
from API_KEY import api_token, api_address
from flask import request, Flask
import requests
import schedule
import time

def database_query():
	# for each request in the database
	# use make_date_object to make a datetime obj
	# see if datetime.now() > datetime obj
	# if Yes, then run send_first_yo(username)
	# and then run the main method

schedule.every(5).minutes.do(database_query)

while True:
	schedule.run_pending()
	time.sleep(1)


def setup(host, path):
	url = 'http://{0}{1}'.format(host, path)


def send_yo_with_link(username, link):
	requests.post(api_address, data={'api_token': api_token, 'username': username, 'link': link});
	return


def send_first_yo(username):
	requests.post(api_address, data={'api_token': api_token, 'username': username});
	return


def make_date_object(date, time):
	return datetime.combine(date, time)

app = Flask(__name__)

def get_location():
	username = request.args.get('username')
	location = request.args.get('location')
	latitude = location.split(';')[0]
	longitude = location.split(';')[1]
	return (latitude, longitude)



if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)






