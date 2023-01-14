# -*- coding: utf-8 -*-
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='a')

logger = logging.getLogger(__name__)

import re
import string
import nltk
import math
import uuid


class Normalization(object):
    def __init__(self, _str, _lenguage):
        self.text = _str
        self.Language = _lenguage.lower()
        self.__lower_text__()
        self.__delete_numbers__()
        self.__delete_punctuation__()

    def __lower_text__(self):
        self.text = self.text.lower()

    def __delete_numbers__(self):
        self.text = re.sub(r'[^\w\s]+|[\d]+', r'', self.text).strip()

    def __delete_punctuation__(self):
        for p in string.punctuation:
            if p in self.text:
                self.text = self.text.replace(p, '')

    def tokenize(self):
        text_tokens = nltk.tokenize.word_tokenize(self.text)
        remove_sw = [word for word in text_tokens if not word in nltk.corpus.stopwords.words(self.Language)]
        legitimatize = nltk.stem.WordNetLemmatizer()
        logging.info(f"Normal END!!!")
        return [legitimatize.lemmatize(word) for word in remove_sw]

class TF_IDF(object):
    def __init__(self, _mas_text, _all_mas_text, ):
        self.sentence = _mas_text
        self.text = _all_mas_text
        pass

    def __counter_met_in_a_sentence__(self, word) -> int:
        counter = 0
        for w in self.sentence:
            if w == word:
                counter += 1

        return counter

    def __counter_quantity_in_text__(self, word) -> int:
        counter = 0
        for sent in self.text:
            for w in sent:
                if w == word:
                    counter += 1
                    break

        return counter

    def return_dict(self) -> dict:
        logging.info(f"TF_IDF END!!!")
        return {word: (self.__counter_met_in_a_sentence__(word) / len(self.sentence)) * (
                math.log(len(self.text)) / self.__counter_quantity_in_text__(word)) for word in self.sentence}

class Lunh(object):
    def __init__(self, _dict_tfidf, _par):
        self.dict_text = _dict_tfidf
        self.par = _par
        self.counter_important_words = self.__the_number_of_important_words_in_the_text__()

    def __counter_the_number_of_important_words_in_the_sentence__(self, dict_sentences) -> int:
        counter = 0
        for word_key in dict_sentences.keys():
            if dict_sentences[word_key] > self.par:
                counter += 1

        return counter

    def __the_number_of_important_words_in_the_text__(self) -> int:
        counter = 0
        for sentences_key in self.dict_text.keys():
            for word_key in self.dict_text[sentences_key].keys():
                if self.dict_text[sentences_key][word_key] > self.par:
                    counter += 1

        return counter

    def __return_sum__(self, dict_sentences) -> int:
        counter = 0
        for word_key in dict_sentences.keys():
            if dict_sentences[word_key] > self.par:
                counter += dict_sentences[word_key]

        return counter

    def return_dict(self) -> dict:
        logging.info(f"Luhn END!!!")
        return {guid: self.__counter_the_number_of_important_words_in_the_sentence__(
            self.dict_text[guid]) * 2 * self.counter_important_words for guid in self.dict_text.keys()}

class Summarizer(object):
    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        pass

    def summarize(self, text, language):

        language_text = language
        split_regex = re.compile(r'[.|!|?|…]')
        sentences = list(filter(lambda t: t, [t.strip() for t in split_regex.split(text)]))
        dict_sentences = {str(uuid.uuid4()): sent for sent in sentences}
        dict_normalise_sentences = {guid: Normalization(dict_sentences[guid], language_text).tokenize() for guid in
                                    dict_sentences.keys()}
        mas_normalize_sentences = [dict_normalise_sentences[guid] for guid in dict_normalise_sentences.keys()]
        dict_tfidf = {guid: TF_IDF(dict_normalise_sentences[guid], mas_normalize_sentences).return_dict() for guid in
                      dict_sentences.keys()}
        dict_lunch = Lunh(dict_tfidf, 0.3).return_dict()
        odd = max([dict_lunch[guid] for guid in dict_lunch.keys()]) * 0.3

        finale_text = ""
        for guid in dict_lunch.keys():
            if dict_lunch[guid] > odd:
                finale_text += (dict_sentences[guid] + '\n')

        return finale_text
