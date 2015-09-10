from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN
from gensim.models import Word2Vec
import os

model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_deps_300D_words.model")
#model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/glove.42B.300d.txt", binary=False)
def wv_synonyms(word):
  if word in model:
    return [x[0] for x in model.most_similar(word)[:5]]
  else:
    return []

def wn_synonyms(ss):
  return [l.name().decode('utf-8') for l in ss.lemmas()]

def wn_getword(s):
  return ss.name().decode('utf-8')

def wn_make_synset(word):
  if '.' in word:
    return wn.synset(word)
  else:
    ss = wn.synsets(word, NOUN)
    if ss:
      return ss[0]
    else:
      return None

for word in ["figuration", "gay.n.01", "portraiture.n.01", "folk_art.n.01", "gender_identity.n.01", "gender.n.02"]:
  

  synonyms = []

  ss = wn_make_synset(word)
  if ss:
    synonyms += wn_synonyms(ss)

  synonyms += wv_synonyms(wn_getword(ss) if ss else word)


  synonyms = list(set(synonyms))

  print word, synonyms
