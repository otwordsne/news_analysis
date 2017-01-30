"""
This will go to the links of the page relevant to your specified homepage. now bloomberg
Give you the top 5 nouns, verbs, adjectives, or top 15 words.
Give you the articles with sentiment above a certain threshold magnitude
"""
from bs4 import BeautifulSoup
#import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import re
import requests
import urllib.request

stopwords = set(['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by',
                'for', 'from', 'has', 'he,', 'in', 'is', 'it',
                'its', "it's", 'of', 'on', 'that', 'the', 'to',
                'was', 'were', 'will', 'with', 'you', 'have', 'been',
                'her', 'hers', 'she', 'him', 'his', 'my', 'mine',
                'this', 'these', 'their', 'theirs', 'them'])

class URL:
    def __init__( self, url):
        self.url = url

    def __str__( self):
        return self.url

    def get_soup( self, url):
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html)
        return soup

def get_soup(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html)
    return soup


def get_news_text(url):
    # html = urllib.urlopen(url)
    soup = get_soup(url)
    body = soup.find('div', attrs={'class': 'body-copy'})
    if body is None:
        print('Article not found.')
        return
    text_w_tags = body.find_all('p', recursive=False)
    text = [x.get_text() for x in text_w_tags]
    text = [re.sub('\n', '', x) for x in text]
    text = [re.sub('\.', '', x) for x in text]
    text = ' '.join(p for p in text)
    return text


def keep_words(text):
    text = text.lower()
    text = re.sub('s&p 500', 's&p500', text)
    return text


def get_keep_words():
    keepwords = set(['s&p500', '&'])
    return keepwords


# Removes the stopwords from
def remove_stopwords(text):
    text = keep_words(text)
    keepwords = get_keep_words()
    # stop = set(stopwords.words('english'))
    # stop = stop.difference(keepwords)
    stop = stopwords
    text = text.lower()
    # tokenizer = get_tokenizer("en_US")
    tokenizer = RegexpTokenizer(r'\w+\&*\w*')
    cleaned_tokens = [str(word) for word in tokenizer.tokenize(text) if word not in stop]
    # cleaned_tokens = [word for word in tokens if word not in stopwords]
    return cleaned_tokens


'''
def remove_links(text):
    webpage = re.compile(r'\s\S*\.[gov|com|org]')
    weird = re.compile('\s\S*\:\S*\s?')
    text = re.sub(webpage, '', text)
    text = re.sub(weird, '', text)
    return text
    # tokens = [toke for toke in tokens if not (webpage.match(toke) or weird.match(toke))]
    # return tokens
'''

def clean_text(text):
    text = re.sub('\u2014','--', text)
    text = remove_stopwords(text)
    # text = remove_links(text)

from nltk.corpus import wordnet

def get_wordnet_pos(word_tag_tuple):
    tag = word_tag_tuple[1]
    if tag.startswith('J'):
        tag = wordnet.ADJ
    elif tag.startswith('V'):
        tag = wordnet.VERB
    elif tag.startswith('N'):
        tag = wordnet.NOUN
    elif tag.startswith('R'):
        tag = wordnet.ADV
    else:
        tag = ''
    return (word_tag_tuple[0], tag)

def main():
    url1 = 'https://www.bloomberg.com/news/articles/2017-01-06/wall-street-is-starting-to-get-nervous-about-all-the-money-pouring-into-u-s-stocks'
    url2 = 'https://www.bloomberg.com/news/articles/2017-01-05/japan-shares-to-drop-on-yen-gain-u-s-jobs-loom-markets-wrap'
    article1 = get_news_text(url1)
    article2 = get_news_text(url2)

    tokenized_txt1 = remove_stopwords(article1)
    tokenized_txt2 = remove_stopwords(article2)

    tagged_txt1 = nltk.pos_tag(tokenized_txt1)
    tagged_txt2 = nltk.pos_tag(tokenized_txt2)
    # print "hi"
    # body = [x.find('div', attrs={'class': 'body-copy'}) for x in article]
    # text_w_tags = body.find_all('p')
    # text = [x.get_text() for x in text_w_tags]
    print(article1)
    print(tokenized_txt1)

    # docs = [tokenized_txt2]
    # dictionary = corpora.Dictionary(docs)
    # doc_term_matrix = [dictionary.doc2bow(doc) for doc in docs]
    # ldamodel = gensim.models.ldamodel.LdaModel(doc_term_matrix, num_topics=10, id2word = dictionary)
    # print(ldamodel.print_topics(num_topics=3, num_words=3))

if __name__ == main():
    main()