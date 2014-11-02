from datetime import datetime
import requests
from yoroApp.API_KEY import api_token, api_address
from yoroApp.models import Note
import yoroApp.eastern_time as eastern_time

for n in Note.objects.all():
	d = n.time
	if datetime.now(tz = eastern_time.Eastern) > d:
		requests.post(api_address, data={'api_token': api_token, 'username': n.user});
