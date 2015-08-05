import csv
import sys
import codecs
import requests
from bs4 import BeautifulSoup
import os

def UnicodeDictReader():
  with open('Artworks.csv', 'rb') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
      yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

for m in UnicodeDictReader():
  url = m['URL']
  oid = m['ObjectID']
  
  fname = os.path.join('extras', oid + '.txt')
  if url and not os.path.isfile(fname):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    txt = soup.find("div", {"class": "body-copy"}).getText().encode('utf-8')
    if txt:
      with open(fname, "w") as tf:
        tf.write(txt)
        print 'writing', fname, len(txt), 'bytes'
