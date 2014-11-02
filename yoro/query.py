import django

from datetime import datetime
import requests
from yoroApp.API_KEY import api_token, api_address
from yoroApp.models import Note
import yoroApp.eastern_time as eastern_time

django.setup()

for n in Note.objects.all():
  d = n.time
  if (not n.flag) and datetime.now(tz = eastern_time.Eastern) > d:
    requests.post(api_address, data={'api_token': api_token, 'username': n.user});
    n.flag = True
    n.save()
    break
