#/data/project/sbl/python/bin/python
from __future__ import unicode_literals
from flask import Flask, request
from wsgiref.handlers import CGIHandler
from werkzeug.debug import DebuggedApplication

import os
import oursql

app = Flask(__name__)

@app.route('/')
def main():
    conn = oursql.Connection(read_default_file=os.path.expanduser('~/.my.cnf'))
    with conn.cursor() as cur:
        cur.execute("select sbl_domain, count(*) from sbl group by sbl_domain order by count(*) desc limit 100;")
        data = cur.fetchall()
    t = ''
    for domain, count in data:
        t += '{0}: {1}'.format(domain, count)
    if not t:
        t = 'No results.'
    return t

CGIHandler().run(DebuggedApplication(app))
