1+1
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib.request
from bs4 import BeautifulSoup
#declaram variabila quote_page1 pentru url-ul paginii
quote_page1 = 'https://www.licori.ro/whisky/1549-glenfiddich-single-malt-scotch-12-ani-700-ml-cutie-metalica.html'
#cu ajutorul urllib.request obtinem pagina HTML a url-ului declarat in variabila quote_page1
page = urllib.request.urlopen(quote_page1)
#declaram variabila soup care contine html-ul paginii
soup = BeautifulSoup(page, 'html.parser')
#obtinem eticheta denumirii produsului, cautand dupa <h1 itemprop="name">
name_box = soup.find('h1', attrs={'itemprop': "name"})
#obtinem textul din interiorul etichetei pentru denumirea produsului (in interiorul variabilei denumire_produs)
denumire_produs1 = name_box.text.strip() 
print (denumire_produs1)

#obtinem eticheta pretului produsului (o stocam in variabila product_box1)
#cautam dupa <span itemprop="price">
product_box1 = soup.find('span', attrs={'itemprop': "price"})
#obtinem textul din interiorul etichetei pentru pretul produsului (pret_produs1)
pret_produs1 = product_box1.text.strip() 
print (pret_produs1)

#obtinem eticheta descrierii produsului, cautand dupa <div class="rte">
name_box3 = soup.find('div', attrs={'class': "rte"})
#stocam textul aferent descrierii produsului in variabila descriere_produs1
descriere_produs1 = name_box3.text.strip() 
print (descriere_produs1)

#obtinem eticheta pentru scurta descriere a produsului (name_box4) si o stocam in interiorul variabilei scurta_descriere_produs1
# cautam dupa <div id="short_description_content">
name_box4 = soup.find('div', attrs={'id': "short_description_content"})
scurta_descriere_produs1 = name_box4.text.strip() 
print (scurta_descriere_produs1)

#obtinem eticheta pentru categoria produsului (name_box5) si o stocam in interiorul variabilei categorie_produs1, apoi o printam (print)
#cautam dupa <span itemprop="title">
name_box5 = soup.find('span', attrs={'itemprop': "title"})
categorie_produs1 = name_box5.text.strip() 
print (categorie_produs1)

#obtinem eticheta fisei tehnice a produsului (name_box6) si o salvam in interiorul variabilei feisa_tehnica_produs1
#cautam dupa <table class="table-data-sheet">
name_box6 = soup.find('table', attrs={'class': "table-data-sheet"})
fisa_tehnica_produs1 = name_box6.text.strip() 
print (fisa_tehnica_produs1)
#exportam datele in format csv,  alaturi de data si ora la care au fost obtinute si salvate in fisier
import csv
from datetime import datetime
with open('produs1.csv', 'a') as csv_file:
 writer = csv.writer(csv_file)
 writer.writerow([denumire_produs1, categorie_produs1, pret_produs1, datetime.now()])

#declaram variabila quote_page2 pentru url-ul paginii pentru cel de-al doilea produs 
quote_page2 = 'https://www.licori.ro/whisky/1551-arran-single-malt-scotch-10-ani-unchillfiltred-700-ml.html'
#cu ajutorul urllib.request obtinem pagina HTML a url-ului declarat in variabila quote_page2
page2 = urllib.request.urlopen(quote_page2)
#declaram variabila soup2 care contine html-ul paginii
soup2 = BeautifulSoup(page2, 'html.parser')
#obtinem eticheta denumirii produsului, cautand dupa <h1 itemprop="name">
name_box1 = soup2.find('h1', attrs={'itemprop': "name"})
#obtinem textul din interiorul etichetei pentru denumirea produsului (in interiorul variabilei denumire_produs2)
denumire_produs2 = name_box1.text.strip() 
print (denumire_produs2)

#obtinem eticheta pentru pretul celui de-al doilea produs
#cautam dupa <span itemprop="price">
name_box2 = soup2.find('span', attrs={'itemprop': "price"})
#obtinem textul din interiorul etichetei pentru pretul produsului (salvam in interiorul variabilei pret_produs2)
pret_produs2 = name_box2.text.strip() 
print (pret_produs2)

#obtinem eticheta pentru descrierea celui de-al doilea produs, cautand dupa <div class="rte">
name_box3 = soup2.find('div', attrs={'class': "rte"})
#salvam in interiorul variabilei descriere_produs2 textul aferent descrierii celui de-al doilea produs
descriere_produs2 = name_box3.text.strip() 
print (descriere_produs2)

#obtinem si salvam eticheta pentru scurta descriere a celui de-al doilea produs 
# cautam dupa <div id="short_description_content">
name_box4 = soup2.find('div', attrs={'id': "short_description_content"})
#salvam scurta descriere a produsului in interiorul variabilei scurta_descriere_produs2
scurta_descriere_produs2 = name_box4.text.strip() 
print (scurta_descriere_produs2)

#obtinem si salvam eticheta categoriei celui de-al doilea produs
#cautam dupa <span itemprop="title">
name_box5 = soup2.find('span', attrs={'itemprop': "title"})
#salvam textul pentru categoria celui de-al doilea produs in interiorul variabilei categorie_produs2
categorie_produs2 = name_box5.text.strip() 
print (categorie_produs2)

#obtinem si salvam eticheta fisei tehnice a celui de-al doilea produs
#cautam dupa <table class="table-data-sheet">
name_box6 = soup2.find('table', attrs={'class': "table-data-sheet"})
#salvam textul atribuit fisei tehnice a celui de-al doilea produs in interiorul variabilei fisa_tehnica_produs2
fisa_tehnica_produs2 = name_box6.text.strip() 
print (fisa_tehnica_produs2)

#exportam datele in format csv,  alaturi de data si ora la care au fost obtinute si salvate in fisier
import csv
from datetime import datetime
with open('produs2.csv', 'a') as csv_file:
 writer = csv.writer(csv_file)
 writer.writerow([denumire_produs2, categorie_produs2, pret_produs2, datetime.now()])
 