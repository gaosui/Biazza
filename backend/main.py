from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import urllib.parse as up
from search import predict
from gensim.models import KeyedVectors

model = KeyedVectors.load("vectors.kv", mmap='r')
print('model loaded')

f = open('cache.json')
cache = json.load(f)
f.close()
print('cache loaded')


def buildDict(cid):
    nrs = []
    posts = []
    for k, v in cache[cid].items():
        nrs.append(k)
        posts.append(v['content'])
    return posts, nrs


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        args = up.parse_qs(self.path.split('?')[1])
        cid = args['cid'][0]

        posts, nrs = buildDict(cid)
        res = predict(posts, nrs, args['key'][0], model)
        objs = []
        for r in res:
            objs.append({
                'nr': r,
                'sub': cache[cid][r]['history'][0]['subject'],
                'short': cache[cid][r]['content'][0:120]
            })

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(objs).encode())
        return


print('start server')
HTTPServer(('', 3000), Handler).serve_forever()
