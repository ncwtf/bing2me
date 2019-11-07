#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import os
import time
from PIL import Image
from io import BytesIO
import win32gui
import win32con
import win32api
import common
import database
import hashlib


def getPicUrl(url):
    print(url)
    r = requests.get(url)
    if not r.ok:
        print(u"ERROR: request %s error %d" % url % r.status_code)
    else:
        bing_content = str(r.content)
        index_of = bing_content.find(common.CONTENT_STR)
        if index_of == -1:
            print(u"ERROR: not found pic url")
        else:
            index_of += len(common.CONTENT_STR)
            pic_url = bing_content[index_of:]
            pic_url = pic_url[: pic_url.index("&rf")]
            return common.WEB_SITE + pic_url


def mkdir(dir_path):
    if not os.path.exists(dir_path):
        print("mkdir %s" % (dir_path))
        os.mkdir(dir_path)


def filemd5(filename):
    if os.path.isfile(filename):
        fp = open(filename, 'rb')
        contents = fp.read()
        fp.close()
        return hashlib.md5(contents).hexdigest()
    else:
        return "error md5"


def savePic(pic_url):
    r = requests.get(pic_url)
    filename = str(time.time()) + ".jpg"
    pic_path = common.BING_PIC_DIR + filename
    if not r.ok:
        print("ERROR: request %s error %d" % pic_url % r.status_code)
    else:
        image = Image.open(BytesIO(r.content))
        image.save(pic_path)
    database.insert(filename, pic_path, filemd5(pic_path))
    return pic_path


def setWallpaper(pic_path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, 1 + 2)


def savePicAndSetWallpaper(pic_url):
    setWallpaper(savePic(pic_url))
