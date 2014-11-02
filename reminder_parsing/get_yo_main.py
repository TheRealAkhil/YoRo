import yelp_api_interface as yelp
import get_category as gc
import category_keywords as ck

"""
Returns a datetime for when the Yo should be sent along with the corresponding yelp link (String)

URL for Yelp matching location within 4000 meters of the area
"""

def get_datetime(reminder_text):
	date = get_category.get_date(text)
	time = get_category.get_time(text)
	return datetime.datetime(date[2],date[0],date[1],time[0],time[1])

def get_yo_main(latitude, longitude, reminder_text):
	reminder_parsed = gc.get_reminder_data(reminder_text)
	category = reminder_parsed["category"] + " " + reminder_parsed["special"]
	if category != "":
		url = yelp.get_yelp_recommendation(category, latitude, longitude)
		return url
	else:
		return "Not Processable"

get_yo_main(41.309882, -72.933874, "i need mexican restaurant for 11/30 1:30 am")




