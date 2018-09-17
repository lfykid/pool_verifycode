# coding:utf-8

import time
import requests
import urllib
from bs4 import BeautifulSoup
import nltk

response = urllib.urlopen('http://php.net/')
html = response.read()
soup = BeautifulSoup(html,'html5lib')
text = soup.get_text(strip=True)

tokens = text.split()

freq = nltk.FreqDist(tokens)
for key, val in freq.items():
    print(str(key) + ':' + str(val))

freq.plot(20, cumulative=False)