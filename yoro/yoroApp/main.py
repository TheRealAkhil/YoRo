from datetime import datetime
from API_KEY import api_token, api_address
from models import Note
import requests
import eastern_time

def database_query():
	for n in Note.objects.all():
		d = n.time
		if datetime.now(tz = eastern_time.Eastern) > d:
			requests.post(api_address, data={'api_token': api_token, 'username': n.user})