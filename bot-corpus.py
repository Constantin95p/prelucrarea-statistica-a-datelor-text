import bs4 as bs
import urllib.request
import re

##########################################################
# Corpus Wikipedia #######################################
##########################################################

wiki_url_list = [
"https://en.wikipedia.org/wiki/Summer_Olympic_Games",
"https://en.wikipedia.org/wiki/1896_Summer_Olympics",
"https://en.wikipedia.org/wiki/1900_Summer_Olympics",
"https://en.wikipedia.org/wiki/1904_Summer_Olympics",
"https://en.wikipedia.org/wiki/1908_Summer_Olympics",
"https://en.wikipedia.org/wiki/1912_Summer_Olympics",
"https://en.wikipedia.org/wiki/1916_Summer_Olympics",
"https://en.wikipedia.org/wiki/1920_Summer_Olympics",
"https://en.wikipedia.org/wiki/1924_Summer_Olympics",
"https://en.wikipedia.org/wiki/1928_Summer_Olympics",
"https://en.wikipedia.org/wiki/1932_Summer_Olympics",
"https://en.wikipedia.org/wiki/1936_Summer_Olympics",
"https://en.wikipedia.org/wiki/1940_Summer_Olympics",
"https://en.wikipedia.org/wiki/1944_Summer_Olympics",
"https://en.wikipedia.org/wiki/1948_Summer_Olympics",
"https://en.wikipedia.org/wiki/1952_Summer_Olympics",
"https://en.wikipedia.org/wiki/1956_Summer_Olympics",
"https://en.wikipedia.org/wiki/1960_Summer_Olympics",
"https://en.wikipedia.org/wiki/1964_Summer_Olympics",
"https://en.wikipedia.org/wiki/1968_Summer_Olympics",
"https://en.wikipedia.org/wiki/1972_Summer_Olympics",
"https://en.wikipedia.org/wiki/1976_Summer_Olympics",
"https://en.wikipedia.org/wiki/1980_Summer_Olympics",
"https://en.wikipedia.org/wiki/1984_Summer_Olympics",
"https://en.wikipedia.org/wiki/1988_Summer_Olympics",
"https://en.wikipedia.org/wiki/1992_Summer_Olympics",
"https://en.wikipedia.org/wiki/1996_Summer_Olympics",
"https://en.wikipedia.org/wiki/2000_Summer_Olympics",
"https://en.wikipedia.org/wiki/2004_Summer_Olympics",
"https://en.wikipedia.org/wiki/2008_Summer_Olympics",
"https://en.wikipedia.org/wiki/2012_Summer_Olympics",
"https://en.wikipedia.org/wiki/2016_Summer_Olympics",
"https://en.wikipedia.org/wiki/2020_Summer_Olympics",

"https://en.wikipedia.org/wiki/Winter_Olympic_Games",
"https://en.wikipedia.org/wiki/1924_Winter_Olympics",
"https://en.wikipedia.org/wiki/1928_Winter_Olympics",
"https://en.wikipedia.org/wiki/1932_Winter_Olympics",
"https://en.wikipedia.org/wiki/1936_Winter_Olympics",
"https://en.wikipedia.org/wiki/1940_Winter_Olympics",
"https://en.wikipedia.org/wiki/1944_Winter_Olympics",
"https://en.wikipedia.org/wiki/1948_Winter_Olympics",
"https://en.wikipedia.org/wiki/1952_Winter_Olympics",
"https://en.wikipedia.org/wiki/1956_Winter_Olympics",
"https://en.wikipedia.org/wiki/1960_Winter_Olympics",
"https://en.wikipedia.org/wiki/1964_Winter_Olympics",
"https://en.wikipedia.org/wiki/1968_Winter_Olympics",
"https://en.wikipedia.org/wiki/1972_Winter_Olympics",
"https://en.wikipedia.org/wiki/1976_Winter_Olympics",
"https://en.wikipedia.org/wiki/1980_Winter_Olympics",
"https://en.wikipedia.org/wiki/1984_Winter_Olympics",
"https://en.wikipedia.org/wiki/1988_Winter_Olympics",
"https://en.wikipedia.org/wiki/1992_Winter_Olympics",
"https://en.wikipedia.org/wiki/1994_Winter_Olympics",
"https://en.wikipedia.org/wiki/1998_Winter_Olympics",
"https://en.wikipedia.org/wiki/2002_Winter_Olympics",
"https://en.wikipedia.org/wiki/2006_Winter_Olympics",
"https://en.wikipedia.org/wiki/2010_Winter_Olympics",
"https://en.wikipedia.org/wiki/2014_Winter_Olympics",
"https://en.wikipedia.org/wiki/2018_Winter_Olympics",
"https://en.wikipedia.org/wiki/2022_Winter_Olympics",
]


# crearea unui fisier gol
with open('corpus-jo.txt', 'w', encoding="utf-8") as f:
	f.write('')

for url in wiki_url_list:
	print('Extragere corpus din URL: ', url)
	raw_html = urllib.request.urlopen(url)
	raw_html = raw_html.read()

	article_html = bs.BeautifulSoup(raw_html, 'lxml')
	article_paragraphs = article_html.find_all('p')
	article_text = ''

	for para in article_paragraphs:
		article_text += para.text

	article_text = article_text.lower()
		
	with open('corpus-jo.txt', 'a', encoding="utf-8") as f:
		f.write(article_text)


##########################################################
# Corpus Locatii in care au avut loc JO ##################
##########################################################

locatii = {}

locatii['Athens'] = 'Greece'
locatii['Paris'] = 'France'
locatii['St. Louis'] = 'United States'
locatii['London'] = 'United Kingdom'
locatii['Stockholm'] = 'Sweden'
locatii['Antwerp'] = 'Belgium'
locatii['Amsterdam'] = 'Netherlands'
locatii['Los Angeles'] = 'United States'
locatii['Berlin'] = 'Germany'
locatii['Helsinki'] = 'Finland'
locatii['Melbourne'] = 'Australia'
locatii['Rome'] = 'Italy'
locatii['Tokyo'] = 'Japan'
locatii['Mexico City'] = 'Mexico'
locatii['Munich'] = 'Germany'
locatii['Montreal'] = 'Canada'
locatii['Moscow'] = 'Russia'
locatii['Los Angeles'] = 'United States'
locatii['Seoul'] = 'South Korea'
locatii['Barcelona'] = 'Spain'
locatii['Atlanta'] = 'United States'
locatii['Sydney'] = 'Australia'
locatii['Beijing'] = 'China'
locatii['Rio de Janeiro'] = 'Brazil'
locatii['Chamonix'] = 'France'
locatii['St. Moritz'] = 'Switzerland'
locatii['Lake Placid'] = 'United States'
locatii['Garmisch-Partenkirchen'] = 'Germany'
locatii['Oslo'] = 'Norway'
locatii["Cortina d'Ampezzo"] = 'Italy'
locatii['Squaw Valley'] = 'United States'
locatii['Innsbruck'] = 'Austria'
locatii['Grenoble'] = 'France'
locatii['Sapporo'] = 'Japan'
locatii['Sarajevo'] = 'Yugoslavia'
locatii['Calgary'] = 'Canada'
locatii['Albertville'] = 'France'
locatii['Lillehammer'] = 'Norway'
locatii['Nagano'] = 'Japan'
locatii['Salt Lake City'] = 'United States'
locatii['Turin'] = 'Italy'
locatii['Vancouver'] = 'Canada'
locatii['Sochi'] = 'Russia'
locatii['Pyeongchang'] = 'South Korea'
locatii['Beijing'] = 'China'

import json
with open('locatii.json', 'w') as fp:
    json.dump(locatii, fp)

