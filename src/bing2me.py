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

WEB_SITE = 'https://cn.bing:.com'
URL_PARAM = "/?scope=web&FORM=HDRSC1"
CONTENT_STR = "data-ultra-definition-src=\""
BING_PIC_DIR = os.path.abspath('.') + "/bing-pic/"


def getPicUrl(url):
    r = requests.get(url)
    if not r.ok:
        print(u"ERROR: request %s error %d" % url % r.status_code)
    else:
        bing_content = str(r.content)
        index_of = bing_content.find(CONTENT_STR)
        if index_of == -1:
            print(u"ERROR: not found pic url")
        else:
            index_of += len(CONTENT_STR)
            pic_url = bing_content[index_of:]
            pic_url = pic_url[: pic_url.index("&rf")]
            return WEB_SITE + pic_url


def mkdir(dir_path):
    if not os.path.exists(dir_path):
        print("mkdir %s" % (dir_path))
        os.mkdir(dir_path)


def savePic(pic_url):
    r = requests.get(pic_url)
    pic_path = BING_PIC_DIR + str(time.time()) + ".jpg"
    if not r.ok:
        print("ERROR: request %s error %d" % pic_url % r.status_code)
    else:
        image = Image.open(BytesIO(r.content))
        image.save(pic_path)
    return pic_path


def setWallpaper(pic_path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, 1 + 2)


def main():
    # init
    print(u'init')
    mkdir(BING_PIC_DIR)
    # request web site
    print(u'request web site %s' % WEB_SITE + URL_PARAM)
    bingPicUrl = getPicUrl(WEB_SITE + URL_PARAM)
    if bingPicUrl is None:
        print(u'not found picture file')
    else:
        # save picture to disk
        print(u'save picture to %s' % BING_PIC_DIR)
        picPath = savePic(bingPicUrl)
        # setup wallpaper
        print(u'setting wallpaper...')
        setWallpaper(picPath)
        print(u'done')


# 程序开始
main()
