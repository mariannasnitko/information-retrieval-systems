import os
import string
import json

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

def read_txt(file_loc):
    file = open(file_loc, encoding='utf8')
    read = file.read()
    file.close()
    return read

def read_db(file_loc):
    if not os.path.isfile(file_loc):
        return {}
    with open(file_loc) as json_file:
        return json.load(json_file)

def write_db(file_loc, data):
    dir = os.path.split(file_loc)[0]
    if len(dir) > 0 and not os.path.exists(dir):
        os.makedirs(dir)
    json_data = json.dumps(data)
    file = open(file_loc, 'w')
    file.write(json_data)
    file.close()

def tokenize(text):
    text = text.lower()
    text_tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in text_tokens if not w in stop_words and not w in string.punctuation]
    return filtered_tokens