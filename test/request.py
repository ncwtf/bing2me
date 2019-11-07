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

ABSPATH = os.path.abspath('.')
WEB_SITE = 'https://cn.bing.com'
CONTENT_STR = "data-ultra-definition-src=\""
BING_HTML_DIR = ABSPATH + "/bing-html/"
BING_PIC_DIR = ABSPATH + "/bing-pic/"


# URL_PARAMS = "&rf=LaDigue_UHD.jpg&pid=hp&w=2880&h=1620&rs=1&c=4"


def get_pic_url(url):
    r = requests.get(url)
    if not r.ok:
        return print("ERROR: request %s error %d" % url % r.status_code)
    else:
        bing_content = str(r.content)
        index_of = len(CONTENT_STR) + bing_content.index(CONTENT_STR)
        pic_url = bing_content[index_of:]
        pic_url = pic_url[: pic_url.index("&rf")]
        return WEB_SITE + pic_url


def mkdir(dir_path):
    if not os.path.exists(dir_path):
        print("mkdir %s" % (dir_path))
        os.mkdir(dir_path)


def save_html(content):
    filename = str(time.time()) + ".html"
    f = open(BING_HTML_DIR + filename, "w")
    f.write(content)
    f.flush()
    f.close()


def save_pic(pic_url):
    r = requests.get(pic_url)
    filename = str(time.time()) + ".jpg"
    if not r.ok:
        print("ERROR: request %s error %d" % pic_url % r.status_code)
    else:
        image = Image.open(BytesIO(r.content))
        a = image.save(BING_PIC_DIR + filename)
        print(a)
    return filename


def set_wallpaper(pic_path):
    print(u'setting wallpaper...')
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, 1 + 2)
    print(u'done')


bing_pic_url = get_pic_url(WEB_SITE + "/?scope=web&FORM=HDRSC1")
mkdir(BING_PIC_DIR)
file_name = save_pic(bing_pic_url)
print(BING_PIC_DIR + file_name)
set_wallpaper(BING_PIC_DIR + file_name)

# request bingIndex
# bing_pic_url = get_pic_url(WEB_SITE + "/?scope=web&FORM=HDRSC1")
# print(bing_pic_url)
# mkdir bing-html dir
# mkdir(BING_HTML_DIR)
# save html file
# save_html(bing_pic_url)
