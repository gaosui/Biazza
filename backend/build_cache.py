from piazza_api import Piazza
from html.parser import HTMLParser
import json


class MyParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.data = []

    def handle_data(self, d):
        self.data.append(d)

    def feed(self, d):
        super().feed(d + '<div>&nbsp;</div>')

    def get_data(self):
        return ''.join(self.data)


f = open('settings.json')
settings = json.load(f)
f.close()

p = Piazza()
p.user_login(settings['email'], settings['pwd'])
cache = {}

for cl in settings['classes']:
    print(cl)
    net = p.network(cl)
    ls = {}
    for post in net.iter_all_posts():
        parser = MyParser()
        parser.feed(post['history'][0]['subject'])
        parser.feed(post['history'][0]['content'])
        for child in post['children']:
            if 'subject' in child:
                parser.feed(child['subject'])
                for cchild in child['children']:
                    parser.feed(cchild['subject'])
            else:
                parser.feed(child['history'][0]['content'])
        ls[post['nr']] = {
            'folders': post['folders'],
            'content': parser.get_data().replace('\n', ' ')
        }
    cache[cl] = ls

f = open('cache.json', 'w')
json.dump(cache, f)
f.close()
