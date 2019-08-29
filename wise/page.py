import re

from .utils import tokenize, remove_stopwords, stem
stem_idx = {}

class Page():
    def __init__(self, title, text, id, dod):
        self.dod = dod
        self.title = title
        self.id = id
        self.stems = []
        self.get_stems(text + " " + title)
        self.index()

    def ret(self):
        return self.dod

    def get_stems(self, text):
        tokens = tokenize(text)
        uniq = remove_stopwords(tokens)
        self.stems = stem(tokens, uniq)

    def index(self):
        for stem in self.stems:
            if stem not in self.dod:
                self.dod[stem] = {self.id : 1}
            
            if stem in self.dod:
                if self.id in self.dod[stem]:
                    self.dod[stem][self.id] += 1
                else:
                    self.dod[stem][self.id] = 1
