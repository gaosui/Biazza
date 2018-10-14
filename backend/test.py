import json
import sys
import search
from gensim.models import KeyedVectors

#model = KeyedVectors.load_word2vec_format("./GoogleNews-vectors-negative300.bin", binary=True)
model = KeyedVectors.load("vectors.kv", mmap='r')

f = open('cache.json')
cache = json.load(f)
f.close()

#for i in range()
cids = list(cache['jml6wogpji0o3'].keys())
posts = []

for i in cids:
    posts.append(cache['jml6wogpji0o3'][str(i)]['content'])

search.setup()
results = search.predict(posts, cids, "test ten runs",model)

for result in results:
    print(cache['jml6wogpji0o3'][result]['content'])
    print()
