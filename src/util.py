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
import bing2me


def makedirs(dir_path):
    if not os.path.exists(dir_path):
        print(u"INFO: util.py - mkdir %s" % (dir_path))
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
        print(u"ERROR: util.py - 请求图片地址: %s 错误, 错误码: %d" % (pic_url, r.status_code))
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


def change_wallpaper():
    # init
    print(u'INFO: main.py - 初始化数据库、图片文件夹')
    database.init()
    makedirs(common.BING_PIC_DIR)
    # request web site
    print(u'INFO: main.py - 请求网址 %s' % common.WEB_SITE + common.URL_PARAM)
    bingPicUrl = bing2me.getPicUrl(common.WEB_SITE + common.URL_PARAM)
    print(u"INFO: 图片URL: %s" % bingPicUrl)
    if bingPicUrl is None:
        print(u'ERROR: main.py - 图片url为None，更换壁纸失败')
    else:
        # save picture to disk and setup wallpaper
        print(u'INFO: main.py - 保存图片，路径 -> %s' % common.BING_PIC_DIR)
        print(u'INFO: main.py - 设置壁纸...')
        savePicAndSetWallpaper(bingPicUrl)
        print(u'INFO: main.py - done')


def save_ico(name):
    ico_path = common.ICONS_DIR + name
    if os.path.exists(ico_path):
        return False
    # 如果文件不存在重新获取
    r = requests.get(common.STATIC_NCWTF_COM + name)
    if not r.ok:
        print(u"ERROR: util.py - 请求icon错误: %s, 错误码: %d" % (common.STATIC_NCWTF_COM + name, r.status_code))
        return False
    else:
        image = Image.open(BytesIO(r.content))
        image.save(ico_path)
        print(u"ICO保存成功，%s" % ico_path)


def get_icons():
    makedirs(common.ICONS_DIR)
    save_ico(common.PANDA_ICO)
    save_ico(common.CHECK_MARK_ICO)
