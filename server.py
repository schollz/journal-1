import os

import markdown
import flask

from pyquery import PyQuery as pq
from flask import Flask, render_template, abort
from flask_common import Common

app = Flask(__name__)
app.debug = True

common = Common(app)

class Entry(object):
    def __init__(self, path):
        self.path = path

    @property
    def html(self):
        with open(self.path, 'rb') as f:
            return markdown.markdown(f.read())

    @property
    def title(self):
        return pq(self.html)('h1')[0].text

    @property
    def slug(self):
        return self.path.split('/')[-1][:-3]

def gen_entry_files():

    files = ['entries/{}'.format(e) for e in os.listdir('entries')]
    for f in reversed(sorted(files, key=os.path.getctime)):
        yield f

def gen_entries():
    for f in gen_entry_files():
        yield Entry(f)


@app.route('/')
def index():

    return render_template('index.html', entries=gen_entries())

@app.route('/entry/<slug>')
def entry(slug):
    try:
        entry = Entry('entries/{}.md'.format(slug))
        return render_template('entry.html', entry=entry, entries=gen_entries())
    except IOError:
        abort(404)

if __name__ == "__main__":
    common.serve()