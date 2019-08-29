import pickle
import os
import os.path
import xml.sax
from collections import Counter

from .page import Page
from .utils import tokenize, remove_stopwords, stem

class InvertedIndex(object):
    def __init__(self):
        self.dod = {}
        self.tid = {}

    def init_parser(self, handler=None):
        xml_parser = xml.sax.make_parser()
        xml_parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        if handler:
            xml_parser.setContentHandler(handler)

        return xml_parser

    def generate_from_dump(self, path_to_dump, handler=None):
        handler = handler if handler else DocumentHandler(self.dod, self.tid)
        self.parser = self.init_parser(handler)
        self.parser.parse(path_to_dump)

    def save_to_file(self, path_to_dir):
        pdump = (self.dod, self.tid)
        fp = os.path.join(path_to_dir, 'index.p')
        pickle.dump(pdump, open(fp, 'wb'))

    def load_from_file(self, path_to_dir):
        fp = os.path.join(path_to_dir, 'index.p')
        self.dod, self.tid = pickle.load(open(fp, 'rb'))

    def search(self, query):
        tokens = tokenize(query)
        tokens = remove_stopwords(tokens)
        stems = stem(tokens, None)
        d1 = {}
        sd1 = set({})

        for each_stem in stems:
            d2 = self.dod.get(each_stem, {})
            sd1 = sd1 | set(d2)
            for each in sd1:
                d1[each] = d1.get(each, 0) + d2.get(each, 0)

        return [self.tid[x[0]] for x in Counter(d1).most_common(10)]



class DocumentHandler(xml.sax.ContentHandler):
    def __init__(self, dod, tid):
        self.dod = dod
        self.tid = tid
        self.curr_id = 0
        self.current_tag = ''
        self.reset()

    def reset(self):
        self.title = ''
        self.text = ''
        self.hashed = 0

    def next_id(self):
        self.curr_id += 1
        return self.curr_id + 1

    # This function is called when the parsing of an element starts
    def startElement(self, tag, attributes):
        self.current_tag = tag

    # This function is called when the parsing of an element ends
    def endElement(self, tag):
        if tag == 'page':
            nid = self.next_id()
            p = Page(self.title.strip(), self.text.strip(), nid, self.dod)
            self.tid[p.id] = p.title
            self.reset()

    # Call when a character is read
    def characters(self, content):
        if self.current_tag == 'title':
          self.title += content

        if self.current_tag == 'text':
          self.text += content
