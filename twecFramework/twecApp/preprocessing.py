"""
    Preprocressing module used for define util function on preprocessing phase of training models
"""
from multiprocessing import Pool
import re
import math
import spacy
from nltk.stem.porter import PorterStemmer

class SimpleSpacyCleaner:
    """
    A simple spacy cleaner that removes stopwords, punctuation, digits and does lemmatization
    """
    def __init__(self, spacy_model):
        """
        Loading the spacy model to clean text
        :param spacy_model: e.g., en_core_web_sm
        """
        self.spacy = spacy.load(spacy_model, disable=["tagger", "parser", "ner"])
        self.spacy.max_length = math.inf

    def clean(self, text, config):
        """
        cleaning text: removing stopwords, punctuation, digits and doing lemmatization
        :param text:
        :return:
        """


        if config['digit_masking']:
            text = digit_masking(text)

        text = " ".join(text.split())

        doc = self.spacy(text)

        tokens = [token for token in doc if
                  not token.is_stop
                  and not token.is_punct]
        if config['lemmatization']:
            tokens = lemmatization(tokens)

        if config['stemming']:
            tokens = stemming(tokens)

        text = " ".join([str(token) for token in tokens])
        if config['lowercasing']:
            text = text.lower()
        return text

    def parallel_cleaner(self, list_of_texts, n_cpus):
        """
        parallel cleaning of texts using Pool
        :param list_of_texts:
        :param n_cpus:
        :return:
        """

        pool = Pool(n_cpus)

        data = pool.map(self.clean, list_of_texts)
        data = [x for x in data if x is not None]
        pool.terminate()
        pool.join()

        return data

def lemmatization(tokens):
    """
        Lemmatization of tokens
        :param tokens:
    """
    return [token.lemma_.strip() for token in tokens]

def stemming(tokens):
    """
        Stemming of tokens, to reducing a word to its root form
        :param tokens:
        :return:
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(str(token)) for token in tokens]

def digit_masking(text):
    """
        Digit masking that transform all digit in token "NUM"
        :param text:
    """
    text_split = text.split()
    tokens = ['NUM' if re.match(r'^-?[0-9]+(\.[0-9]+)?$', token)
              else token
              for token in text_split]
    return " ".join(tokens)
