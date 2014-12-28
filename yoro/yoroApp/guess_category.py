"""
Function that guesses the category for a noun that is not known - assumes the noun has lost plural

Assumes that the noun is not found within the keyword categorization

Then looks up in dictionary, extracts subject/nouns, and then repeats until it hits keyword or calls three times
If still not found, then just return the noun itself

The dictionary used is provided by adambom on GitHub (adambom/dictionary). The following is the dictionary text used:
"https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json"
"""
import urllib2
import json
import ast
import cPickle
import os.path
from nltk.data import load

import os

#current_dir = os.getcwd()

#out = open ("tet.txt", "wb")
#out.write(os.getcwd())

#os.chdir(current_dir)

from category_keywords import keyword_categorization
known_cats_dict = {}
for tup in keyword_categorization:
	known_cats_dict[tup[0]] = tup[1]

dict_format = None
if os.path.exists("dictionary.pickle"):
	dict_format = cPickle.load(open("dictionary.pickle","rb"))
else:
	info = urllib2.urlopen("https://raw.githubusercontent.com/adambom/dictionary/master/dictionary.json")
	dictionary_text = None
	for line in info:
		dictionary_text = line ##gets dictionary
	dict_format = ast.literal_eval(dictionary_text)
	cPickle.dump(dict_format, open("dictionary.pickle", "wb" ))

def guess_category_list(noun, iterations_left): #includes part of speech
	if iterations_left == 0 or noun == "":
		return []
	noun = noun.encode("ascii","ignore").upper()
	definition = None
	if noun not in dict_format: #it is either plural or not in
		if noun[-1] == "S":
			if noun[:-1] in dict_format:
				definition = dict_format[noun[:-1]]
			elif len(noun) > 2 : 
				if noun[-2] == "E" and noun[:-2] in dict_format:
					definition = dict_format[noun[:-2]]
	else:
		definition = dict_format[noun]
	if definition == None:
		return []
	#### extract nouns from the definition, and then check if in the keyword dictionary
	for char in "!@#$%^&*()><?|}{~`,;":
		definition = definition.replace(char," ")
	definition_words =definition.split(".")[0].split(" ") # first sentence's words	
	pos_tagger = cPickle.load('nltk_english_pos.pickle') #the file is form the nltk package
	tags = pos_tagger.tag(definition_words) #nltk
	def_nouns = []
	results_tot = []
	for tag in tags:
		if tag[1] in ["NN", "NNS", "NNPS", "NNP"]:
			def_nouns.append(tag[0].lower())
	for def_noun in def_nouns:
		if def_noun in known_cats_dict:
			results_tot.append(known_cats_dict[def_noun])
		else:
			try:
				results_tot.extend(guess_category_list(def_noun, iterations_left - 1))
			except UnicodeDecodeError:
				return []
	return results_tot

def guess_category(noun):
	list_of_guesses = guess_category_list(noun,3)
	if list_of_guesses == []:
		return ""
	guess_dict = {}
	for guess in list_of_guesses:
		if guess not in guess_dict:
			guess_dict[guess] = 1
		else:
			guess_dict[guess] += 1
	guess_count_list = [(guess,guess_dict[guess]) for guess in guess_dict]
	guess_count_list.sort(key = lambda x: x[1])
	print guess_count_list
	return guess_count_list[-1][0]

# os.chdir(current_dir)
