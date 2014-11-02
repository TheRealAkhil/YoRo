"""
Process the user reminder and decompose into features:
- Date, Time of request
- Category of the request: (Can Add to List)
	1. Groceries + Convenience Store
	2. Clothes and Apparel
	3. Bank/Withdrawals
	4. Restaurants

Returns a Dictionary:

dict {
	"date": List of ints [11,1,2014]. If yr ends in two digits, add 20 to front
	"time": String (Military Time resolved to minutes --> "14:00" == 2 PM)
	"category" : String 
	"specifics" : An optional argument that offers extra detail for category Ex: "Indian Restaurant"
}

Much of this code relies from and is adapted from the nltk library in python, as indicated.

"""
from nltk.metrics.distance import edit_distance #from nltk
from nltk.stem.porter import PorterStemmer #from nltk
from category_keywords import keyword_categorization
import datetime
import re
import eastern_time

##taken from the nltk corpora
nltk_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
nltk_stopwords = set(nltk_stopwords)

# return a string MM/DD/YYYY
def get_date(text):
	current_date = datetime.datetime.today().isoformat()
	date_calced = None
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	month_date_format = "\d+/\d+"
	month_date_year_format =  "[0-9]+/[0-9][0-9]?/[0-9]+"
	month_date_no_abbrev = "(January|February|March|April|May|June|July|August|September|October|November|December) \d+"
	month_date_year_no_abbrev = "(January|February|March|April|May|June|July|August|September|October|November|December) \d\d? \d+ "
	tomorrow = "tomorrow"
	regex_list = [ month_date_year_format, month_date_format, month_date_year_no_abbrev, month_date_no_abbrev, tomorrow ]
	for regex in regex_list:
		re_compile = re.compile(regex, re.IGNORECASE)
		result = re_compile.search(text)
		if result and date_calced == None:
			date_calced = result.group(0)
	###parse current date
	parts = current_date.split("-")
	remove_time = [parts[1],parts[0]]
	remove_time.extend((parts[2].split("T")))
	if date_calced == None:
		return [int(remove_time[0]), int(remove_time[2]), int(remove_time[1])]
	elif "/" in date_calced:
		parts_backslash = date_calced.split("/") 
		if len(parts_backslash) == 3:
			if int(parts_backslash[2]) < 100:
				return [int(parts_backslash[0]), int(parts_backslash[1]), int(parts_backslash[2]) + 2000]
			else:
				return [int(parts_backslash[0]), int(parts_backslash[1]), int(parts_backslash[2])]
		else:
			return [int(parts_backslash[0]), int(parts_backslash[1]), int(remove_time[1])]
	elif "tomorrow" in date_calced.lower():
		today = datetime.datetime.today()
		one_day = datetime.timedelta(days = 1)
		tomorrow = (today + one_day).isoformat()
		parts = tomorrow.split("-")
		remove_time = [parts[1],parts[0]]
		remove_time.extend((parts[2].split("T")))
		return [int(remove_time[0]), int(remove_time[2]), int(remove_time[1])]
	else:
		parts_backslash = date_calced.split(" ") 
		if len(parts_backslash) == 3:
			return [int(months.index(parts_backslash[0])) + 1, int(parts_backslash[1]), int(parts_backslash[2])]
		else:
			return [int(months.index(parts_backslash[0])) + 1, int(parts_backslash[1]), int(remove_time[1])]

def is_adjective(word):
	#adjective endings
	#http://www.grammar-quizzes.com/adj-forms.html
	adjective_endings = ["ary","ful","ic","ical","ish","less","ian","ly","ous","can"]
	for end in adjective_endings:
		if len(word) < len(end):
			continue
		else:
			if word[len(word) - len(end):] == end:
				return True
	return False

def get_time(text):
	pm_format = "\d\d?(:\d\d)? ?pm"
	am_format = "\d\d?(:\d\d)? ?am"
	time_calced = None
	regex_list = [am_format,pm_format]
	for regex in regex_list:
		re_compile = re.compile(regex, re.IGNORECASE)
		result = re_compile.search(text)
		if result and time_calced == None:
			time_calced = result.group(0)
	if time_calced == None:
		return [23,59]
	time_calced = time_calced.upper()
	if ":" not in time_calced:
		integer_time = int(time_calced.replace("A","").replace("P","").replace("M",""))
		if "PM" in time_calced and integer_time != 12:
			return [integer_time + 12,0]
		else:
			if integer_time == 12:
				if "PM" in time_calced:
					return [12,0]
				else:
					return [0,0]
			else:
				return [integer_time,0]
	else:
		integer_time = int(time_calced.replace("A","").replace("P","").replace("M","").split(":")[0])
		minutes = time_calced.replace("A","").replace("P","").replace("M","").split(":")[1].strip()
		if "PM" in time_calced and integer_time != 12:
			return [integer_time + 12, int(minutes)]
		elif "PM" in time_calced and integer_time == 12:
			return [integer_time, int(minutes)]
		else:
			if integer_time == 12:
				return [0,int(minutes)]
			else:
				return [integer_time, int(minutes)]

def close_enough(string1, string2): #are two works close enough that we can consider them equal
	stemmer = PorterStemmer() #from nltk
	string1 = stemmer.stem(string1).encode("ascii","ignore")
	string2 = stemmer.stem(string2).encode("ascii","ignore")
	return ((edit_distance(string1, string2, transpositions=True) < max(len(string1 + string2)/10,2))) and ((string1[0] == string2[0]) and (string1[1] == string2[1]))
	 #error as a ratio of the length of the strings

def get_key_words(text):
	tokens = text.split(" ")
	stemmed_tokens = []
	
	stemmer = PorterStemmer() #from nltk
	preserved_tokens = []
	for word in tokens:
		if word not in nltk_stopwords:
			stemmed_tokens.append(stemmer.stem(word).encode("ascii","ignore")) #from nltk
			preserved_tokens.append(word) #need to preserve the stem of the adjective
	category = ""
	special = ""
	for i in range(len(stemmed_tokens)):
		for word in keyword_categorization:
			should_break = False
			if close_enough(word[0], stemmed_tokens[i]):
				category = word[1]
				should_break = True
			if i > 0:
				if is_adjective(preserved_tokens[i-1]):
					special = preserved_tokens[i-1]  
			if should_break: break
	if category == "":
		special = ""
	return { "category": category, "special" :special}

def get_reminder_data(text):
	date = get_date(text)
	time = get_time(text)

	dict_info = get_key_words(text)
	category = dict_info["category"]
	special = dict_info["special"]
	return  {
		"datetime" : datetime.datetime(date[2],date[0],date[1],time[0],time[1], tzinfo = eastern_time.Eastern),
		"category" : category,
		"special" : special
	}





 


