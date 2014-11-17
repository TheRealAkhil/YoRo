import django

from datetime import datetime
import requests
from yoroApp.API_KEY import api_token, api_address
from yoroApp.models import Note
import yoroApp.eastern_time as eastern_time
import threading

django.setup()

class dbQuery(threading.Thread):    
  def __init__(self):
    threading.Thread.__init__(self)
    self._finished = threading.Event()
    self._interval = 15.0
    
  def shutdown(self):
    self._finished.set()
    
  def run(self):
    while True:
      if self._finished.isSet(): return
      self.task()
      
      # sleep for interval or until shutdown
      self._finished.wait(self._interval)
    
  def task(self):
  	for n in Note.objects.all():
		  d = n.time
		  if (not n.flag) and datetime.now(tz = eastern_time.Eastern) > d:
		    requests.post(api_address, data={'api_token': api_token, 'username': n.user});
		    n.flag = True
		    n.save()
		    break
