import yelp_api_interface as yelp
import get_category as gc
import category_keywords as ck

"""
Returns a datetime for when the Yo should be sent along with the corresponding yelp link (String)

URL for Yelp matching location within 4000 meters of the area
"""

def get_yo_main(latitude, longitude, reminder_text):
	print latitude, longitude, reminder_text
	reminder_parsed = gc.get_reminder_data(reminder_text)
	category = reminder_parsed["category"] + "" + reminder_parsed["special"]
	datetime = reminder_parsed["datetime"]
	if category != "":
		url = yelp.get_yelp_recommendation(category, latitude, longitude)
		print datetime
		print url
		return url, datetime
	else:
		return "Not Processable"

get_yo_main(41.309882, -72.933874, "remind me to buy eggs at 3 PM tomorrow")



