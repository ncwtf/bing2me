#!/usr/bin/python

import sqlite3


def connect():
    conn = sqlite3.connect('bing2me.db')
    print(u"INFO: database.py - 打开数据库连接")
    return conn


def init():
    conn = connect()
    c = conn.cursor()
    try:
        c.execute('''
        CREATE TABLE pic
            (id         INT     PRIMARY KEY     NOT NULL,
            filename    VARCHAR(50)                NOT NULL,
            path        TEXT                    NOT NULL,
            md5         VARCHAR(50)                NOT NULL);
        ''')
    except:
        print(u"INFO: database.py - 表创建失败，或已存在")
        return False
    print(u"INFO: database.py - 表创建完成")
    conn.commit()
    conn.close()


def insert(filename, path, md5):
    conn = connect()
    c = conn.cursor()
    sql = "INSERT INTO pic (id, filename, path, md5) VALUES (%d, '%s', '%s', '%s')"
    values = (nextId(), filename, path, md5)
    print(u"INFO: database.py - [%s]" %(sql % values))
    c.execute(sql % values)
    conn.commit()
    conn.close()


def getOne(result):
    column = None
    for row in result:
        column = row[0]
    return column


def nextId():
    conn = connect()
    c = conn.cursor()
    result = c.execute("select id from pic ORDER BY id DESC limit 1")
    id = getOne(result)
    return 1 if id == None else (id + 1)


def selectCountByMd5(md5):
    conn = connect()
    c = conn.cursor()
    result = c.execute("select count(id) from pic where md5 = '%s'" % md5)
    count = getOne(result)
    return count
