#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bing2me
import common
import database
import util


def main():
    # init
    print(u'INFO: main.py - 初始化数据库、图片文件夹')
    database.init()
    util.mkdir(common.BING_PIC_DIR)
    # request web site
    print(u'INFO: main.py - 请求网址 %s' % common.WEB_SITE + common.URL_PARAM)
    bingPicUrl = bing2me.getPicUrl(common.WEB_SITE + common.URL_PARAM)
    if bingPicUrl is None:
        print(u'ERROR: main.py - 图片url为None，更换壁纸失败')
    else:
        # save picture to disk and setup wallpaper
        print(u'INFO: main.py - 保存图片，路径 -> %s' % common.BING_PIC_DIR)
        print(u'INFO: main.py - 设置壁纸...')
        util.savePicAndSetWallpaper(bingPicUrl)
        print(u'INFO: main.py - done')


# 程序开始
main()
