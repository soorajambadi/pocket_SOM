__author__ = 'tintin'
from nltk.stem.wordnet import WordNetLemmatizer
import lxml.html
import nltk
from bs4 import BeautifulSoup
import pdb
import string
import requests
#import time
#pdb.set_trace()


class CrawlerException(Exception):
    pass


class CrawlerPageNotFound(CrawlerException):
    def __init__(self, msg):
        self.msg = msg


class PageTitleNotFound(CrawlerException):
    def __init__(self, msg):
        self.msg = msg


class WebPage():
    def __init__(self, url, crawler):
        self.url = url
        self.crawler = crawler
        self.content = None

    def get_page_contents(self):
        if self.content:
            return self.content
        else:
            self.title, self.content = self.crawler.get_page_contents(self.url)


class Crawler():
    def __init__(self):
        self.stop_words = []
        try:
            fp = open("neo4j/stop", "r")
            word_list = fp.readlines()
            for word in word_list:
                self.stop_words.append(word.replace('\n', ""))
            fp.close()
        except IOError:
            word_list = []

    def make_a_page(self, url):
        page = WebPage(url, self)
        return page

    def get_page_contents(self, url):
        #a['url']['summary'],a['url']['title'], a['url']['tags']
        header = {'User-agent': 'Mozilla/5.0'}
        try:
            html = requests.get(url, headers = header).text
        except:
            raise CrawlerPageNotFound("Page Not Found")
        pg = lxml.html.document_fromstring(html)
        try:
            title = pg.find(".//title").text
        except:
            raise PageTitleNotFound("Title Not found")
            title = url
        try:
            texts = self.getTextHTML(html)
            texts = texts.replace("\t", '')
            texts = texts.replace("\n", '')
            texts = texts.replace("\r", '')
            stem_visible_text = self.stem_Text(texts)
            stem_visible_text = self.getClearText(stem_visible_text, self.stop_words)
            return title, stem_visible_text
        except:
            print("Exception occured in get_page_contents")

    def stem_Text(self, texts):
        stemmer = WordNetLemmatizer()
        stem_visible_text = ""
        # text after stemming
        texts = texts.lower()
        for text in texts.split():
            if text[:4] != "http:" or text[:5] != "https:":
                stem_visible_text = stem_visible_text + " " + stemmer.lemmatize(text)
        texts = ""
        for text in stem_visible_text.split():
            if text not in self.stop_words:
                texts = texts + " " + text
        stem_visible_text = texts
        return stem_visible_text

    #getClearText is used by getAllTags for getting clear text from stem_visible_text

    def getClearText(self, stem_visible_text, stop_words):
        compare_text = ""
        for t in stem_visible_text.split():
            for p in string.punctuation:
                t = t.replace(p, "")
            if not t.isdigit():
                compare_text = compare_text + " " + t
        return compare_text


# strips the html and gets only the content stripping the tags.
    def getTextHTML(self, html):
        soup = BeautifulSoup(html)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text