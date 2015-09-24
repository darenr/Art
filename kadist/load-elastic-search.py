from elasticsearch import Elasticsearch
import json
import sys
import codecs
import itertools
import urllib3
from textblob import TextBlob, Word
from textblob.wordnet import Synset

def is_synset(w):
  return 'n.0' in w

def wn_hypernym(w):
 ss = Synset(w)
 return [s._name for s in ss.hypernyms()]


urllib3.disable_warnings()


es = Elasticsearch()


def load_data(filename):
  index = 'kadist'
  doc_type = 'kadist_art_collection'
  if es.indices.exists(index=index):
    print es.indices.delete(index=index)

  request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
  }

  print es.indices.create(index=index, body = request_body)

  schema = {
        'mappings': {
          doc_type: {
            "properties" : {
              "worktype" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "collection" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "decade" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "major_tags" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "minor_tags" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "mlt_hypernyms" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "artist_name" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "id" : {
                "store":  "true",
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "imgurl" : {
                "store":  "true",
                "type" :    "string",
                "stored" : "yes",
                "index":    "no"
              },
              "description": {
                "store":  "true",
                "type" :    "string"
              }
            }
          }
        }
      }

  print es.indices.put_mapping(index=index, doc_type=doc_type, body=schema['mappings'] )

  with codecs.open(filename, 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      if 'imgurl' in m and m['imgurl']:
        m['imgurl'] = m['imgurl'].split('?')[0]

      if len(m['major_tags']) or len(m['minor_tags']):
        m['mlt_tags'] = ' '.join([x.replace('.','') for x in m['major_tags']+m['minor_tags']])
      else:
        blob = TextBlob(' '.join([m['artist_name'], m['description']]))
        m['mlt_tags'] = ' '.join([x for x in blob.noun_phrases if blob.noun_phrases.count(x) > 0])

      m['collection'] = 'Kadist'
      m['decade'] = int(m['year'] / 10)*10

      # create hypernym synsets
      major = list(itertools.chain.from_iterable([wn_hypernym(w) for w in m['major_tags'] if is_synset(w)]))
      minor = list(itertools.chain.from_iterable([wn_hypernym(w) for w in m['minor_tags'] if is_synset(w)]))
      m['mlt_hypernyms'] = ' '.join([x.replace('.','') for x in major+minor])

      try:
        es.index(index=index, doc_type=doc_type, id=m['id'], body=m)
      except KeyboardInterrupt:
        raise
      except:
        print m



if len(sys.argv) != 2:
  print 'usage: <kadist.json>'
  sys.exit(-1)
else:
  load_data(sys.argv[1])
