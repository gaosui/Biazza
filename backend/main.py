from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import urllib.parse as up


f = open('cache.json')
cache = json.load(f)
f.close()
classCode = None


def search(key, dict):
    pass


def buildDict(cid):
    res = {}
    for k, v in cache[cid].items():
        res[k] = v['content']
    return res


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        args = up.parse_qs(self.path.split('?')[1])

        dic = buildDict(args['cid'][0])
        search(args['key'][0], dic)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        return


HTTPServer(('', 3000), Handler).serve_forever()
