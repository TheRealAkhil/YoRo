import yelp_api_interface as yelp
import get_category as gc
import get_category_new as gc_new
import category_keywords as ck
import eastern_time

"""
Returns a datetime for when the Yo should be sent along with the corresponding yelp link (String)

URL for Yelp matching location within 8000 meters of the area
"""

import datetime
import os

# os.chdir("/Users/Akhil/Desktop/Hackathons/yoro/yoro/yoroApp")

#gives the EST timestamp of the Yo
def get_datetime(reminder_text):
	date = gc.get_date(reminder_text)
	time = gc.get_time(reminder_text)
	return datetime.datetime(date[2],date[0],date[1],time[0],time[1],tzinfo = eastern_time.Eastern)

#parsers and gives a consise summary of the reminder - should be used in html file in initial yo sent
def get_subject(text):
	return gc_new.get_reminder_text(text)

#returns the url for the yelp page, or "Not Processable" if no url can be obtained
def get_yo_main(latitude, longitude, reminder_text):
	category = gc_new.obtain_yelp_category(reminder_text)
	if category == "":
		return "http://espn.go.com"
	url = yelp.get_yelp_recommendation(category, latitude, longitude)
	return url

latitude = 42

latitude = 42.357721
longitude= -71.094334
text = "remind me to buy a basketball at 11:52PM today"

print get_yo_main(latitude, longitude, text)
