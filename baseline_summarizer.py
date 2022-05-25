# -*- coding: utf-8 -*-
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='a')
logger = logging.getLogger(__name__)

import re
import string
import nltk
import cld2
import os
import math
import uuid

class Normalization(object):
	def __init__(self,_str,_lenguage):
		self.text = _str
		self.Language = _lenguage.lower()
		self.__lower_text__()
		self.__dalete_numbers__()
		self.__dalete_punctuation__()

	def __lower_text__(self):
		self.text = self.text.lower()

	def __dalete_numbers__(self):
		self.text = re.sub(r'[^\w\s]+|[\d]+', r'',self.text).strip()

	def __dalete_punctuation__(self):
		for p in string.punctuation:
			if p in self.text:
				self.text = self.text.replace(p, '')

	def __return_language_of_text__(self,_str):
		return cld2.detect(_str)[2][0][0]

	def tokenize(self):
		text_tokens = nltk.tokenize.word_tokenize(self.text)
		remove_sw = [word for word in text_tokens if not word in nltk.corpus.stopwords.words(self.Language)]
		#snow_stemmer = nltk.stem.snowball.SnowballStemmer(language=self.Language)
		lemmatizer = nltk.stem.WordNetLemmatizer()
		logging.info(f"Normal END!!!")
		return [lemmatizer.lemmatize(word) for word in remove_sw]


class TF_IDF(object):
	def __init__(self,_mas_text,_all_mas_text,):
		self.sentence = _mas_text
		self.text = _all_mas_text
		pass

	def __counter_met_in_a_sentence__(self,word) -> int:
		counter = 0
		for w in self.sentence:
			if(w == word):
				counter+=1

		return counter

	def __counter_quantity_in_text__(self,word) -> int:
		counter = 0
		for sent in self.text:
			for w in sent:
				if(w==word):
					counter+=1
					break

		return counter

	def return_dict(self) -> dict:
		logging.info(f"TF_IDF END!!!")
		return {word:(self.__counter_met_in_a_sentence__(word)/len(self.sentence))*(math.log(len(self.text))/self.__counter_quantity_in_text__(word)) for word in self.sentence}


class Lunh(object):
	def __init__(self,_dict_tfidf,_par):
		self.dict_text = _dict_tfidf
		self.par = _par
		self.counter_important_words = self.__the_number_of_important_words_in_the_text__()

	def __counter_the_number_of_important_words_in_the_sentence__(self,dict_sentences) -> int:
		counter = 0
		for word_key in dict_sentences.keys():
			if(dict_sentences[word_key] > self.par):
				counter+=1

		return counter

	def __the_number_of_important_words_in_the_text__(self) -> int:
		counter = 0
		for sentences_key in self.dict_text.keys():
			for word_key in self.dict_text[sentences_key].keys():
				if self.dict_text[sentences_key][word_key] > self.par:
					counter+=1

		return counter

	def __return_sum__(self,dict_sentences) -> int:
		counter = 0
		for word_key in dict_sentences.keys():
			if(dict_sentences[word_key] > self.par):
				counter += dict_sentences[word_key]

		return counter

	def return_dict(self)->dict:
		logging.info(f"Luhn END!!!")
		return {guid:self.__counter_the_number_of_important_words_in_the_sentence__(self.dict_text[guid])*2*self.counter_important_words for guid in self.dict_text.keys()}
		#return {guid:self.__return_sum__(self.dict_text[guid]) for guid in self.dict_text.keys()}

#language_text = cld2.detect(text)[2][0][0]
#split_regex = re.compile(r'[.|!|?|…]')
#sentences = list(filter(lambda t: t, [t.strip() for t in split_regex.split(text)]))
#dict_sentences = {str(uuid.uuid4()):sent for sent in sentences}
#dict_noramalase_sentences = {guid:Normalization(dict_sentences[guid],language_text).tokenize() for guid in dict_sentences.keys()}
#print(dict_sentences)
#mas_normalaze_sentences = [dict_noramalase_sentences[guid] for guid in dict_noramalase_sentences.keys()]

#dict_tfidf = {guid:TF_IDF(dict_noramalase_sentences[guid],mas_normalaze_sentences).return_dict() for guid in dict_sentences.keys()}

#print(dict_tfidf)

#dict_lunh = Lunh(dict_tfidf,0.7).return_dict()

#odd = max([dict_lunh[guid] for guid in dict_lunh.keys()])*0.3
#for guid in dict_lunh.keys():
#	if dict_lunh[guid] > odd:
#		print(dict_sentences[guid])

#print(dict_lunh)
#s = Normalization(text,language_text).tokenize()
#print(s)

class Summarizer(object):
	def __init__(self):
		pass

	def initels(self):
		nltk.download('stopwords')
		nltk.download('punkt')
		nltk.download('wordnet')
		nltk.download('omw-1.4')
		open("init.txt",'w')
	def chec_init(self) -> bool:
		return (False,True)['init.txt' in os.listdir()]

	def _summariz_(self,path_text):
		if(not(self.chec_init())):
			print("Initialize, additional data not uploaded")
			print("Use <<<python app.py init>>>")
			return

		with open(path_text,'r',encoding='utf-8') as f:
			text = f.read()

		language_text = cld2.detect(text)[2][0][0]
		split_regex = re.compile(r'[.|!|?|…]')
		sentences = list(filter(lambda t: t, [t.strip() for t in split_regex.split(text)]))
		dict_sentences = {str(uuid.uuid4()):sent for sent in sentences}
		dict_noramalase_sentences = {guid:Normalization(dict_sentences[guid],language_text).tokenize() for guid in dict_sentences.keys()}
		mas_normalaze_sentences = [dict_noramalase_sentences[guid] for guid in dict_noramalase_sentences.keys()]
		dict_tfidf = {guid:TF_IDF(dict_noramalase_sentences[guid],mas_normalaze_sentences).return_dict() for guid in dict_sentences.keys()}
		dict_lunh = Lunh(dict_tfidf,0.7).return_dict()
		odd = max([dict_lunh[guid] for guid in dict_lunh.keys()])*0.3

		with open(path_text.split('.')[0]+'abstract.txt','w',encoding='utf-8') as f:
			for guid in dict_lunh.keys():
				if dict_lunh[guid] > odd:
					f.write(dict_sentences[guid]+'\n')