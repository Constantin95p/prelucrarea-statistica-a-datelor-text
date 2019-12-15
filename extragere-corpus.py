import bs4 as bs
import urllib.request
import re


raw_html = urllib.request.urlopen('https://en.wikipedia.org/wiki/Football')
raw_html = raw_html.read()

article_html = bs.BeautifulSoup(raw_html, 'lxml')

article_paragraphs = article_html.find_all('p')

article_text = ''

for para in article_paragraphs:
	article_text += para.text

article_text = article_text.lower()
	
with open('corpus.txt', 'w', encoding="utf-8") as f:
	f.write(article_text)
