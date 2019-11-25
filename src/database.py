#!/usr/bin/python

import sqlite3
import common
import log

logger = log.LOGGER


def connect():
    conn = sqlite3.connect(common.DATABASE_PATH)
    logger.info(u"打开数据库连接")
    return conn


def create_table(sql):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute(sql)
    except:
        logger.info(u"表创建失败，或已存在")
        return False
    logger.info(u"表创建完成")
    conn.commit()
    conn.close()


def getOne(result):
    column = None
    for row in result:
        column = row[0]
    return column


def init():
    Pic().create_pic()
    Pid().create_pid()


class Pic:
    def create_pic(self):
        create_table('''
        CREATE TABLE pic
            (id         INT     PRIMARY KEY     NOT NULL,
            filename    VARCHAR(50)                NOT NULL,
            path        TEXT                    NOT NULL,
            md5         VARCHAR(50)                NOT NULL);
        ''')

    def insert(self, filename, path, md5):
        conn = connect()
        c = conn.cursor()
        sql = "INSERT INTO pic (id, filename, path, md5) VALUES (%d, '%s', '%s', '%s')"
        values = (self.nextId(), filename, path, md5)
        logger.info(u"[%s]" % (sql % values))
        c.execute(sql % values)
        conn.commit()
        conn.close()

    def nextId(self):
        conn = connect()
        c = conn.cursor()
        result = c.execute("select id from pic ORDER BY id DESC limit 1")
        id = getOne(result)
        return 1 if id == None else (id + 1)

    def selectCountByMd5(self, md5):
        conn = connect()
        c = conn.cursor()
        result = c.execute("select count(id) from pic where md5 = '%s'" % md5)
        count = getOne(result)
        return count


class Pid:
    def create_pid(self):
        create_table('''
        CREATE TABLE pid
            (id         INT     PRIMARY KEY     NOT NULL,
            pid         VARCHAR(10)             NOT NULL);
        ''')

    def count(self):
        c = connect().cursor()
        return getOne(c.execute("select count(id) from pid where id = 1"))

    def get(self):
        c = connect().cursor()
        pid = getOne(c.execute("select pid from pid where id = 1"))
        return None if pid is None else int(pid)

    def put(self, p_id):
        conn = connect()
        c = conn.cursor()
        if self.count() < 1:
            sql = "INSERT INTO pid (id, pid) VALUES (1, '%s')"
        else:
            sql = "UPDATE pid SET pid = '%s' WHERE id = 1 "
        logger.info(u"[%s] params[%s]" % (sql, p_id))
        c.execute(sql % p_id)
        conn.commit()
        conn.close()
