"""
Use of Yelp API to search for nearby businesses matching a keyword

Most of this document is from: https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py. the Yelp API
Code Example Document
"""

###Begin code from https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py
### Source: Yelp API Documentation

import argparse
import json
import pprint
import sys
import urllib
import urllib2
import geopy
import oauth2

import YELP_API_KEY

API_HOST = 'api.yelp.com'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users. (filled by Tejas)
CONSUMER_KEY = YELP_API_KEY.Consumer_Key
CONSUMER_SECRET = YELP_API_KEY.Consumer_Secret
TOKEN = YELP_API_KEY.Token
TOKEN_SECRET = YELP_API_KEY.Token_Secret

def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, path)

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, location, lat, longi):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'latitude': lat, ##added
        'longitude': longi, ##added
        'radius_filter': 5000, ##added
        'sort':0
        #'category_filter': category
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location)

    businesses = response.get('businesses')

    if not businesses:
        return

    business_id = businesses[0]['id']


    response = get_business(business_id)

### End code from https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py

def get_yelp_recommendation(category, latitude, longitude ):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim() ##from geopy source documentation
    geocode_loc = geolocator.reverse(str(latitude) + ", " + str(longitude))
    city = geocode_loc.address.split(",")[-5].encode("ascii", "ignore").strip() ##obtain the city    
    response = search(category, city, latitude, longitude) 
    businesses = response["businesses"]
    if len(businesses) < 1:
        return ""
    else:
        top_business = businesses[0]
        return top_business["mobile_url"]

