from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import urllib.parse as up
from search import predict
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format(
    "./GoogleNews-vectors-negative300.bin", binary=True)
print('model loaded')

f = open('cache.json')
cache = json.load(f)
f.close()
print('cache loaded')


def buildDict(cid):
    cids = list(cache[cid].keys())
    posts = []
    for i in cids:
        posts.append(cache[cid][str(i)]['content'])
    return posts, cids


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        args = up.parse_qs(self.path.split('?')[1])

        posts, cids = buildDict(args['cid'][0])
        res = predict(posts, cids, args['key'], model)
        print(res)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        return


print('start server')
HTTPServer(('', 3000), Handler).serve_forever()
