import json
import sys


f = open('cache.json')
cache = json.load(f)
f.close()


print(cache['jml6wogpji0o3'][sys.argv[1]]['content'])

#from http.server import BaseHTTPRequestHandler, HTTPServer


# class Handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         print(self.path.split('/')[-1])
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.end_headers()
#         return


# HTTPServer(('', 3000), Handler).serve_forever()
