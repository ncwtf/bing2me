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
import database
import common


def mkdir(dir_path):
    if not os.path.exists(dir_path):
        print(u"INFO: util.py - mkdir %s" % (dir_path))
        os.mkdir(dir_path)


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
        print(u"ERROR: util.py - 请求图片地址: %s 错误, 错误码: %d" % pic_url % r.status_code)
        return False
    else:
        image = Image.open(BytesIO(r.content))
        image.save(pic_path)
        md5_str = filemd5(pic_path)
        if database.selectCountByMd5(md5_str) < 1:
            database.insert(filename, pic_path, md5_str)
            return pic_path
        else:
            os.remove(pic_path)
            print(u"INFO: util.py - md5 已存在. 删除图片文件.")
            return False


def savePicAndSetWallpaper(pic_url):
    pic_path = savePic(pic_url)
    if not pic_path:
        print(u"INFO: util.py - 壁纸没有更换.")
    else:
        setWallpaper(pic_path)
