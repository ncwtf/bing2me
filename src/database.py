#!/usr/bin/python

import sqlite3


def connect():
    conn = sqlite3.connect('bing2me.db')
    print("Opened database successfully")
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
        print("Create table failed")
        return False
    print("Table created successfully")
    conn.commit()
    conn.close()
    print("Database closed")


def insert(filename, path, md5):
    conn = connect()
    c = conn.cursor()
    # sql = "INSERT INTO pic (id, filename, path, md5) VALUES ("
    # sql += str(nextId()) + ","
    # sql += filename + ","
    # sql += path + ","
    # sql += md5 + ")"
    # c.execute(sql)
    sql = "INSERT INTO pic (id, filename, path, md5) VALUES (%d, '%s', '%s', '%s')"
    values = (nextId(), filename, path, md5)
    print(sql % values)
    c.execute(sql % values)
    conn.commit()
    conn.close()
    print("Database closed")


def nextId():
    conn = connect()
    c = conn.cursor()
    result = c.execute("select id from pic ORDER BY id DESC limit 1")
    id = None
    for a in result:
        id = a[0]
    return 1 if id == None else (id + 1)
