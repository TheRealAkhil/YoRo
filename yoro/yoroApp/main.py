from datetime import datetime
from API_KEY import api_token, api_address
from flask import request, Flask
from models import Note
import requests
import schedule
import time
import get_yo_main

def database_query():
	# for each request in the database
	# use make_date_object to make a datetime obj
	# see if datetime.now() > datetime obj
	# if Yes, then run send_first_yo(username)
	# and then run the main method
	for n in Note.objects.all():
		d = n.time
		if datetime.now() > d:
			send_first_yo(n.user)


schedule.every(5).minutes.do(database_query)

while True:
	schedule.run_pending()
	time.sleep(1)

def send_yo_with_link(username, link):
	requests.post(api_address, data={'api_token': api_token, 'username': username, 'link': link});
	return


def send_first_yo(username):
	requests.post(api_address, data={'api_token': api_token, 'username': username});
	return


def make_date_object(date, time):
	return datetime.combine(date, time)

app = Flask(__name__)

@app.route("/yo/")
def main_yo():
	username = request.args.get('username')
	location = request.args.get('location')
	latitude = location.split(';')[0]
	longitude = location.split(';')[1]

	# go through database
	# and search for the text
	# of the input corresponding
	# with username, assign to var
	# reminder_text
	reminder_text = None

	for n in Note.objects.all():
		if username == n.user:
			reminder_text = n.text_body
			break

	yo_url = get_yo_main(latitude, longitude, reminder_text)[0]
	send_yo_with_link(username, yo_url)	



if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)