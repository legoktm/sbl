from __future__ import unicode_literals

import datetime
import phpserialize
import os
import oursql
import urlparse
from wmflabs import db

import_query = """
SELECT log_params
FROM logging
WHERE log_type="spamblacklist"
AND log_timestamp > ?
AND log_timestamp < ?;
"""

dump_query = """
INSERT INTO `sbl` VALUES(?, ?, ?, ?, ?);
"""

conn = oursql.Connection(read_default_file=os.path.expanduser('~/.my.cnf'))


def get_hostname(url):
    return urlparse.urlparse(url).netloc


def get_all_db_names():
    with db.connect('meta_p') as cur:
        cur.execute('SELECT dbname from wiki')
        r = cur.fetchall()
    for w in r:
        yield w[0]


def dump(dbname, urls):
    p = []
    for url in urls:
        p.append((
            None,
            dbname,
            get_hostname(url),
            url,
            0,
        ))
    with conn.cursor() as cur:
        cur.executemany(dump_query, p)


def get_cur_ts():
    return datetime.datetime.now().strftime('"%Y%m%d%H%M%S"')


def import_from_db(dbname, old=0, cur=get_cur_ts()):
    with db.connect(dbname) as cur:
        cur.execute(import_query, (ts,cur))
        res = cur.fetchall()
    urls = []
    for x in res:
        ser = x[0]
        data = phpserialize.loads(ser)
        urls.append(data['4::url'])
    dump(dbname, urls)


if __name__ == '__main__':
    path = os.path.expanduser('~/lastrun.ts')
    if os.path.exists(path):
        with open(path) as f:
            ts = int(f.read())
    else:
        ts = 0
    cur = get_cur_ts()
    for dbname in get_all_db_names():
        if dbname != 'centralauth':
            print dbname
            import_from_db(dbname, ts, cur)
    with open(path, 'w') as f:
        f.write(str(cur))


