import urllib.request
from bs4 import BeautifulSoup
import bs4
import csv

counter = 0
page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jack-jones-hello-nov-mmse-m')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        pret = produs.find('span', class_='campaign-discount')
        pret_final = pret.strong.get_text()[:-6].replace('.', '')+','+pret.strong.get_text()[-6:]
        print('Pret produs:', pret_final)
        with open('baza-date-01.csv', 'a', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([brand_name.get_text(), descriere.get_text(), float(pret_final[:-4].replace(',', '.'))])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jack-jones-hello-nov-mmse-m?page=2')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        pret = produs.find('span', class_='campaign-discount')
        pret_final = pret.strong.get_text()[:-6]+','+pret.strong.get_text()[-6:]
        print('Pret produs:', pret_final)
        with open('baza-date.csv', 'a', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([brand_name.get_text(), descriere.get_text(), float(pret_final[:-4].replace(',', '.'))])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jack-jones-hello-nov-mmse-m?page=3')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        pret = produs.find('span', class_='campaign-discount')
        pret_final = pret.strong.get_text()[:-6]+','+pret.strong.get_text()[-6:]
        print('Pret produs:', pret_final)
        with open('baza-date.csv', 'a', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([brand_name.get_text(), descriere.get_text(), float(pret_final[:-4].replace(',', '.'))])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jack-jones-hello-nov-mmse-m?page=4')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        pret = produs.find('span', class_='campaign-discount')
        pret_final = pret.strong.get_text()[:-6]+','+pret.strong.get_text()[-6:]
        print('Pret produs:', pret_final)
        with open('baza-date.csv', 'a', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([brand_name.get_text(), descriere.get_text(), float(pret_final[:-4].replace(',', '.'))])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jack-jones-hello-nov-mmse-m?page=5')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        pret = produs.find('span', class_='campaign-discount')
        pret_final = pret.strong.get_text()[:-6]+','+pret.strong.get_text()[-6:]
        print('Pret produs:', pret_final)
        with open('baza-date.csv', 'a', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([brand_name.get_text(), descriere.get_text(), float(pret_final[:-4].replace(',', '.'))])
        counter += 1

        print('---------------------')

page_url = urllib.request.urlopen('https://www.fashiondays.ro/s/jack-jones-hello-nov-mmse-m?page=6')
soup_url = BeautifulSoup(page_url, 'html.parser')
produse = soup_url.find('ul', attrs={'id': 'products-listing-list'}).li.next_siblings
for produs in produse:
    if type(produs) is not bs4.element.NavigableString:
        brand_name = produs.find('span', class_='brand-name')
        print('Brand:', brand_name.get_text())
        descriere = produs.find('span', class_='product-description')
        print('Descriere produs:', descriere.get_text())
        pret = produs.find('span', class_='campaign-discount')
        pret_final = pret.strong.get_text()[:-6]+','+pret.strong.get_text()[-6:]
        print('Pret produs:', pret_final)
        with open('baza-date.csv', 'a', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([brand_name.get_text(), descriere.get_text(), float(pret_final[:-4].replace(',', '.'))])
        
        counter += 1

        print('---------------------')

print('S-au afisat', counter, 'produse')
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from scipy.stats import pearsonr
from scipy.stats import chi2_contingency
from scipy import array
from scipy import stats
import numpy as np
import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.formula.api import ols
ais = pd.read_csv('baza-date-01.csv')
ais.columns = ['Brand', 'Produs', 'Pret']
ais.info()
ais['Pret'] = ais['Pret'].fillna(0).astype(np.int64)
ais['Pret'] = ais['Pret'].astype(np.int64)
ais = ais.loc[ais['Pret']>0]
#Statistica descriptiva pentru Pret
print(ais.describe())
print(ais.Pret.describe())
##Media: În medie, pretul produselor este de 480.545064 lei.
##Quartila 1: 25% dintre produse costa pana in 319.00 lei, iar restul de 75% costa peste 319.00 lei.
## Quartila 3: 75% dintre produse costa pana in 579.00 lei, iar restul de 25% costa peste 579.00 lei.
##Abaterea standard: În medie, pretul produselor variază cu 226.589903 lei față de nivelul mediu.
print(ais.dtypes)
print(ais.Pret.describe())
print('Mediana preturilor este', ais.Pret.median())
##Mediana: 50% dintre produse costa până în 449.0 lei, iar restul de 50% de peste 469 lei.
from scipy.stats import mode
print(mode(ais.Pret))
##Modul: Cele mai multe produse costa 469 lei.
from scipy.stats import skew
print('Coeficientul de asimetrie Skewness este', skew(ais.Pret))
##Skweness: Coeficientul de asimetrie=2.062215 arată faptul că distribuția este asimetrică la dreapta.
from scipy.stats import kurtosis
print('Coeficientul de boltire kurtosis este', kurtosis(ais.Pret))
##Kurtosis: Coeficientul de boltire=8.2384051 arată faptul că distribuția este leptocurtica.
import numpy as np
import matplotlib.pyplot as plt
plt.hist(ais.Pret, bins='auto')
##Această histogramă evidențiază faptul că distribuția preturiloreste asimetrică la dreapta, adică majoritatea produselor înregistrează o valoare scazuta a acestei variabile (Pret)(majoritatea produselor sunt ieftine).
plt.boxplot(ais.Pret)
##Diagrama boxplot aferentă pretului produselor oferă următoarele informații: minimul (199 lei), Quartila 1 (319 lei), mediana (449 lei), Quartila 3 (579 lei). Exista outlieri (valori extreme).
