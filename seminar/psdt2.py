import urllib.request
from bs4 import BeautifulSoup
import bs4
import sys

counter = 0
page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jeans-epic-mmse-m')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        descriere = produs.find('span', class_='campaign-discount')
        print('Pret produs:', descriere.strong.get_text()[:-6]+','+descriere.strong.get_text()[-6:])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jeans-epic-mmse-m?page=2')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        descriere = produs.find('span', class_='campaign-discount')
        print('Pret produs:', descriere.strong.get_text()[:-6]+','+descriere.strong.get_text()[-6:])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jeans-epic-mmse-m?page=3')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        descriere = produs.find('span', class_='campaign-discount')
        print('Pret produs:', descriere.strong.get_text()[:-6]+','+descriere.strong.get_text()[-6:])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jeans-epic-mmse-m?page=4')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        descriere = produs.find('span', class_='campaign-discount')
        print('Pret produs:', descriere.strong.get_text()[:-6]+','+descriere.strong.get_text()[-6:])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jeans-epic-mmse-m?page=5')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        descriere = produs.find('span', class_='campaign-discount')
        print('Pret produs:', descriere.strong.get_text()[:-6]+','+descriere.strong.get_text()[-6:])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jeans-epic-mmse-m?page=6')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        descriere = produs.find('span', class_='campaign-discount')
        print('Pret produs:', descriere.strong.get_text()[:-6]+','+descriere.strong.get_text()[-6:])
        counter += 1

        print('---------------------')

print('S-au afisat', counter, 'produse')

