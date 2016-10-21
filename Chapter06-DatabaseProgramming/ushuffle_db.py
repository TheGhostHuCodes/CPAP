#!/usr/bin/env python3

import os
from random import randrange as rand

COLSIZ = 10
FIELDS = ('login', 'userid', 'projid')
RDBMS = {'s': 'sqlite'}
DBNAME = 'test'
DBUSER = 'root'
DB_EXC = None
NAMELEN = 16

tformat = lambda s: str(s).title().ljust(COLSIZ)
cformat = lambda s: s.upper().ljust(COLSIZ)


def setup():
    return RDBMS[input("""
Choose a database system:

    (S)QLite

Enter Choice: """).strip().lower()[0]]


def connect(db, DBNAME):
    global DB_EXC
    dbDir = '%s_%s' % (db, DBNAME)

    if db == 'sqlite':
        try:
            import sqlite3
        except ImportError:
            return None
        DB_EXC = sqlite3
        if not os.path.isdir(dbDir):
            os.mkdir(dbDir)
        cxn = sqlite3.connect(os.path.join(dbDir, DBNAME))

    else:
        return None
    return cxn


def create(cur):
    try:
        cur.execute(
            '''CREATE TABLE users (login VARCHAR(%d), userid INTEGER, projid INTEGER)'''
            % NAMELEN)
    except DB_EXC.OperationalError:
        drop(cur)
        create(cur)


drop = lambda cur: cur.execute('DROP TABLE users')

NAMES = (('aaron', 8312), ('angela', 7603), ('dave', 7306), ('davina', 7902),
         ('elliot', 7911), ('ernie', 7410), ('jess', 7912), ('jim', 7512),
         ('larry', 7311), ('leslie', 7808), ('melissa', 8602), ('pat', 7711),
         ('serena', 7003), ('stan', 7607), ('faye', 6812), ('amy', 7209),
         ('mona', 7404), ('jennifer', 7608))


def randName():
    pick = set(NAMES)
    while pick:
        yield pick.pop()


def insert(cur, db):
    if db == 'sqlite':
        cur.executemany("INSERT INTO users VALUES(?,?,?)",
                        [(who, uid, rand(1, 5)) for who, uid in randName()])


getRC = lambda cur: cur.rowcount if hasattr(cur, 'rowcount') else -1


def update(cur):
    fr = rand(1, 5)
    to = rand(1, 5)
    cur.execute("UPDATE users SET projid=%d WHERE projid=%d" % (to, fr))
    return fr, to, getRC(cur)


def delete(cur):
    rm = rand(1, 5)
    cur.execute('DELETE FROM users WHERE projid=%d' % rm)
    return rm, getRC(cur)


def dbDump(cur):
    cur.execute('SELECT * FROM users')
    print("\n%s" % "".join(map(cformat, FIELDS)))
    for data in cur.fetchall():
        print("".join(map(tformat, data)))


def main():
    db = setup()
    print("*** Connect to %r database" % db)
    cxn = connect(db, DBNAME)
    if not cxn:
        print("ERROR: %r not supported or unreachable, exit" % db)
        return
    cur = cxn.cursor()

    print("\n*** Creating users table")
    create(cur)

    print("\n*** Inserting names into table")
    insert(cur, db)
    dbDump(cur)

    print("\n*** Randomly moving folks")
    fr, to, num = update(cur)
    print("\t(%d users moved) from (%d) to (%d)" % (num, fr, to))
    dbDump(cur)

    print("\n*** Randomly choosing group")
    rm, num = delete(cur)
    print("\t(group #%d; %d users removed)" % (rm, num))
    dbDump(cur)

    print("\n*** Dropping users table")
    drop(cur)
    print("\n*** Close cxns")
    cur.close()
    cxn.commit()
    cxn.close()


if __name__ == '__main__':
    main()
