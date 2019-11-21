#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os
import hashlib
import time
from PIL import Image
from io import BytesIO
import win32gui
import win32con
import win32api
import database as db
import common
import bing_request as br
import psutil
import sys
import log

logger = log.LOGGER


def makedirs(dir_path):
    if not os.path.exists(dir_path):
        logger.info(u"mkdir %s" % (dir_path))
        os.makedirs(dir_path)


def md5(contents):
    return hashlib.md5(contents).hexdigest()


def filemd5(filename):
    if os.path.isfile(filename):
        fp = open(filename, 'rb')
        contents = fp.read()
        fp.close()
        return md5(contents)
    else:
        return "error md5"


def setWallpaper(pic_path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, 1 + 2)


def savePic(pic_url):
    r = requests.get(pic_url)
    filename = str(time.time()) + ".jpg"
    pic_path = common.BING_PIC_DIR + filename
    if not r.ok:
        logger.error(u"请求图片地址: %s 错误, 错误码: %d" % (pic_url, r.status_code))
        return False
    else:
        image = Image.open(BytesIO(r.content))
        image.save(pic_path)
        md5_str = filemd5(pic_path)
        if db.Pic().selectCountByMd5(md5_str) < 1:
            db.Pic().insert(filename, pic_path, md5_str)
            return pic_path
        else:
            os.remove(pic_path)
            logger.info(u"md5 已存在. 删除图片文件.")
            return False


def savePicAndSetWallpaper(pic_url):
    pic_path = savePic(pic_url)
    if not pic_path:
        logger.info(u"壁纸没有更换.")
    else:
        setWallpaper(pic_path)


def change_wallpaper():
    # request web site
    logger.info(u'请求网址 %s' % common.WEB_SITE + common.URL_PARAM)
    bingPicUrl = br.getPicUrl(common.WEB_SITE + common.URL_PARAM)
    logger.info(u"图片URL: %s" % bingPicUrl)
    if bingPicUrl is None:
        logger.error(u'图片url为None，更换壁纸失败')
    else:
        # save picture to disk and setup wallpaper
        logger.info(u'保存图片，路径 -> %s' % common.BING_PIC_DIR)
        logger.info(u'设置壁纸...')
        savePicAndSetWallpaper(bingPicUrl)
        logger.info(u'done')


def save_ico(name):
    ico_path = common.ICONS_DIR + name
    if os.path.exists(ico_path):
        return False
    # 如果文件不存在重新获取
    r = requests.get(common.STATIC_NCWTF_COM + name)
    if not r.ok:
        logger.error(u"请求icon错误: %s, 错误码: %d" % (common.STATIC_NCWTF_COM + name, r.status_code))
        return False
    else:
        image = Image.open(BytesIO(r.content))
        image.save(ico_path)
        logger.info(u"ICO保存成功，%s" % ico_path)


def get_icons():
    makedirs(common.ICONS_DIR)
    save_ico(common.PANDA_ICO)
    save_ico(common.CHECK_MARK_ICO)


def suicider():
    db_pid = db.Pid().get()
    logger.info(u"db_pid: %s, file_name: %s" % (db_pid, common.FILE_NAME))
    if db_pid is not None and psutil.pid_exists(db_pid):
        p = psutil.Process(db_pid)
        if p.name() == common.FILE_NAME:
            logger.info(u"suicider")
            sys.exit()
    else:
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == common.FILE_NAME:
                db.Pid().put(pid)
                logger.info(u"update")
