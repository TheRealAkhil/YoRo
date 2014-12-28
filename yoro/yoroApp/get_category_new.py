"""
Contains methods to 
1) Obtain the subject of a free text entry
2) Obtain any modifiers for the entry
3) Identify the category of store that subject belongs to
"""

#Loading modules
from nltk.data import load
from nltk.metrics.distance import edit_distance #from nltk
from nltk.stem.porter import PorterStemmer #from nltk
from guess_category import guess_category

import numpy

import cPickle

import os

string=  os.path.dirname(os.path.realpath("query.py"))
print string

# current_dir = os.getcwd()

# os.chdir("/Users/Akhil/Desktop/Hackathons/yoro/yoro/yoroApp")


#tokenizer = load('nltk_tokenizer_english.pickle') #the file is form the nltk package
pos_tagger = cPickle.load(open("nltk_english_pos.pickle", "rb")) #the file is form the nltk package
# print pos_tagger
text = "remind me to get 6 eggs at 3 PM tomorrow"

# obtain part of speech tags for words
def tag_words(text):
	for char in "!@#$%^&*()><?|}{~`":
		text = text.replace(char," ")
	words = text.split(" ")
	tags = pos_tagger.tag(words) #nltk
	return tags

#common words in reminders that should be omitted
omit_list = ["remind", "PM", "AM", "tomorrow", "remember", ""]
omit_list = [word.upper() for word in omit_list]

#prunes the tag list to retain the relevant words (nouns, verbs, adjectives)
def get_relevant_words(tags):
	relevant_words = [] #only adjectives, nouns, verbs
	for i in range(len(tags)):
		tag = tags[i]
		relevant_list = ["JJ","NN","VBN","VBG", "CD", "VB", "NNS", "NNP", "NNPS"]
		relevant_word = False
		for chars in relevant_list:
			if chars == tag[1]:
				relevant_word = True
		if tags[0] == "":
			relevant_word = False
		if relevant_word:
			if tag[0].upper() not in omit_list:
				relevant_words.append(tag[0])
	return relevant_words

def close_enough(string1, string2): #are two works close enough that we can consider them equal
	return ((edit_distance(string1, string2, transpositions=True) < max(len(string1 + string2)/10,1))) and ((string1[0] == string2[0]) and (string1[1] == string2[1]))

# returns true of the reminder should return a Yelp or not. For example "walking the dog" doesn't need a Yelp link, but 
# "buying groceries would be useful"
def should_yelp(tags): 
	# any synonym of "buy", "get", "obtain", or no verb at all should receive a yelp at all
	# all synonyms are from dictionary.com
	stemmer = PorterStemmer() #from nltk
	contains_verb = False
	verbs = set(["acquire","pick", "buy", "procure", "redeem", "shop", "get", "gain", "purchase", "obtain", "take", "reserve"])
	for tag in tags:
		if tag[1] in ["VBN","VBG","VB", "IN"]:
			contains_verb = True
			tag_text = tag[0].lower()
			stemmed_verb = stemmer.stem(tag_text).encode("ascii","ignore")
			for verb in verbs:
				if close_enough(stemmed_verb, verb):
					return True
	return not contains_verb

#get the "core" of the reminder, which we can assume to be list of words between the first and last important word, inclusive
def obtain_reminder_text(tags, important_words):
	words_to_keep = []
	print important_words
	if len(important_words) < 2:
		return " ".join(important_words)
	else:
		collect_word = False
		for tag in tags:
			if tag[0] == important_words[0]:
				collect_word = True
			if collect_word:
				words_to_keep.append(tag[0])
			if tag[0] == important_words[-1]:
				collect_word = False
	return " ".join(words_to_keep)
	
#obtains the nouns for a given document
def get_search_text(tags):
	verb_2 = ["acquire","pick", "buy", "procure", "redeem", "shop", "get", "gain", "purchase", "obtain", "take", "reserve"]
	nouns = []
	modifiers = []
	index = 0
	for tag in tags:
		if tag[1] in ["NN", "NNS", "NNP", "NNPS"] and (not (tag[0].upper() in omit_list)) and (not (tag[0].lower() in verb_2)) :
			nouns.append((tag[0],index))
		index += 1
	for noun in nouns:
		i = noun[1]
		if i == 0:
			poss_i = [1]
		elif i == len(tags) - 1:
			poss_i = [len(tags) - 2]
		else:
			poss_i = [i + 1, i -1]
		for val in poss_i:
			if val >= 0 and val < len(tags):
				if tags[val][1] == "JJ":
					modifiers.append(tags[val][0].lower())
	return [x[0] for x in nouns], " ".join(modifiers)

#obtains different permutations of the word that are pretty close.
# conditions: ends and begins with correct letters
# only applicable to words of len 5 or greater

def get_mispellings(word):
	word = word.lower()
	autocorrect_nearby_dict =  {} #matches key to key that's close by o keyboard
	autocorrect_nearby_dict["q"] = ["aws"]
	autocorrect_nearby_dict["a"] = ["qwsxz"]
	autocorrect_nearby_dict["x"] = ["zsdc"]
	autocorrect_nearby_dict["z"] = ["xsa"]
	autocorrect_nearby_dict["s"] = ["awdx"]
	autocorrect_nearby_dict["d"] = ["sxcfrew"]
	autocorrect_nearby_dict["e"] = ["wsdfr"]
	autocorrect_nearby_dict["c"] = ["xdfv"]
	autocorrect_nearby_dict["f"] = ["derg"]
	autocorrect_nearby_dict["v"] = ["xdfv"]
	autocorrect_nearby_dict["f"] = ["zsdc"]
	autocorrect_nearby_dict["r"] = ["edfgt"]
	autocorrect_nearby_dict["v"] = ["cfgb"]
	autocorrect_nearby_dict["g"] = ["fvbht"]
	autocorrect_nearby_dict["x"] = ["zsdc"]
	autocorrect_nearby_dict["t"] = ["rfghy"]
	autocorrect_nearby_dict["y"] = ["tghju"]
	autocorrect_nearby_dict["h"] = ["gbnjy"]
	autocorrect_nearby_dict["n"] = ["bhjm"]
	autocorrect_nearby_dict["j"] = ["nhkmu"]
	autocorrect_nearby_dict["u"] = ["hijy"]
	autocorrect_nearby_dict["j"] = ["uikm"]
	autocorrect_nearby_dict["k"] = ["uioljm"]
	autocorrect_nearby_dict["m"] = ["nkj"]
	autocorrect_nearby_dict["l"] = ["mkop"]
	autocorrect_nearby_dict["p"] = ["ol"]
	autocorrect_nearby_dict["w"] = ["qase"]
	autocorrect_nearby_dict["i"] = ["ujko"]
	autocorrect_nearby_dict["o"] = ["iklp"]
	autocorrect_nearby_dict["b"] = ["vghn"]
	if len(word) < 6:
		return [word]
	else:
		words_list = [word]
		for i in range(len(word)):
			if i != 0 and i != len(word) - 1 and i != 1 :
				substitutes = autocorrect_nearby_dict[word[i]]
				substitutes = [letter for letter in substitutes[0]] + [""]
				for char in substitutes:
					words_list.append(word[:i] + char + word[i+1:])
		return list(set(words_list))

#returns a dictionary: {"subject" : subject, "category": category, "should_yelp", True or False}
from category_keywords import keyword_categorization
known_cats_dict = {}
for tup in keyword_categorization:
	known_cats_dict[tup[0]] = tup[1]

# obtains the category for a noun
def get_category_noun(noun):
	category = None
	autocorrect_nouns = get_mispellings(word)
	if noun in known_cats_dict:
		category = known_cats_dict[noun]
		return category
	else:
		for possible in autocorrect_nouns:
			if possible in known_cats_dict:
				category = known_cats_dict[possible]
				return category
		return guess_category(noun) # a function that will input a noun that is not in the database, and will guess




def get_reminder_text(text):
	tags = tag_words(text)
	tags = tag_words(text)
	rel_words = get_relevant_words(tags)
	rem_text = obtain_reminder_text(tags, rel_words)
	return rem_text

#"" if default yelp should be given ("grocery"), anything else: category + modifier text
#
def obtain_yelp_category(text):
	text = text.lower()
	tags = tag_words(text)
	return_yelp = should_yelp(tags)
	nouns, modifier_text = get_search_text(tags)
	if len(nouns) == 0:
		return ""
	list_of_guesses = [get_category_noun(x) for x in nouns]
	guess_dict = {}
	for guess in list_of_guesses:
		if guess not in guess_dict:
			guess_dict[guess] = 1
		else:
			guess_dict[guess] += 1
	guess_count_list = [(guess,guess_dict[guess]) for guess in guess_dict]
	guess_count_list.sort(key = lambda x: x[1])
	return guess_count_list[-1][0] + " " + modifier_text

# uses tagger to decide part of speech
"""
Info from: http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
CC, Coordinating conjunction],
["CD"	Cardinal number
3.	DT	Determiner
4.	EX	Existential there
5.	FW	Foreign word
6.	IN	Preposition or subordinating conjunction
7.	JJ	Adjective
8.	JJR	Adjective, comparative
9.	JJS	Adjective, superlative
10.	LS	List item marker
11.	MD	Modal
12.	NN	Noun, singular or mass
13.	NNS	Noun, plural
14.	NNP	Proper noun, singular
15.	NNPS	Proper noun, plural
16.	PDT	Predeterminer
17.	POS	Possessive ending
18.	PRP	Personal pronoun
19.	PRP$	Possessive pronoun
20.	RB	Adverb
21.	RBR	Adverb, comparative
22.	RBS	Adverb, superlative
23.	RP	Particle
24.	SYM	Symbol
25.	TO	to
26.	UH	Interjection
27.	VB	Verb, base form
28.	VBD	Verb, past tense
29.	VBG	Verb, gerund or present participle
30.	VBN	Verb, past participle
31.	VBP	Verb, non-3rd person singular present
32.	VBZ	Verb, 3rd person singular present
33.	WDT	Wh-determiner
34.	WP	Wh-pronoun
35.	WP$	Possessive wh-pronoun
36.	WRB	Wh-adverb
"""

# os.chdir(current_dir)



