from datetime import datetime
from API_KEY import api_token, api_address
from flask import request
import requests

# @return current date & time in a datetimeobject
def get_current_date():
	return datetime.now()

# sends a Yo with link to username
# @param username -> username to to be Yo'ed
# @param link -> link to be attached to Yo
def send_yo_with_link(username, link):
	requests.post(api_address, data={'api_token': api_token, 'username': username, 'link': link});
	return

# sends a Yo to username
# @param username -> username to be Yo'ed
def send_yo(username):
	requests.post(api_address, data={'api_token': api_token, 'username': username});
	return

# makes a datetime object with both date and time attributes
# @param date -> a datetime date object (datetime.date(year, month, day))
# @param time -> a datetime time object (datetime.time(hour, minute))
# @return a datetime object with both date and time
def make_date_object(date, time):
	return datetime.combine(date, time)

# Handle callback request
# @return a tuple of (latitude, longitude) of user's location
def get_location():
	username = request.args.get('username')
	location = request.args.get('location')
	latitude = location.split(';')[0]
	longitude = location.split(';')[1]
	return (latitude, longitude)

send_yo_with_link('ultraman', 'http://www.nba.com')
get_location()





