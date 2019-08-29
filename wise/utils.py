import re
from os.path import abspath, dirname, join
import pickle
from Stemmer import Stemmer
stemmer = Stemmer('english')

stop_words = abspath(join(dirname(__file__), 'stopwords.p'))
with open(stop_words, 'rb') as fp:
    stopwords = pickle.load(fp)

tokenize_reg = re.compile(
    r'-| |,|\(|\)|\||\{|\}|\]|\[|@|#|\t|\n|\<..*\>|=|/|\.|\'|\"|:')

def tokenize(text):
    return [x for x in tokenize_reg.split(text.lower()) if x]

def remove_stopwords(tokens):
    fs = set(tokens)
    fs.difference(stopwords)
    return fs

stem_map = {}
def stem(tokens, uniq):
        stems = []
        for token in tokens:
            if uniq is not None and token not in uniq:
                continue
            if token in stem_map:
                stem = stem_map[token]
            else:
                stem = stemmer.stemWord(token)
                stem_map[token] = stem
            stems.append(stem_map[token])
        return stems
