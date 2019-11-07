#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bing2me
import common
import database


def main():
    # init
    print(u'init')
    database.init()
    bing2me.mkdir(common.BING_PIC_DIR)
    # request web site
    print(u'request web site %s' % common.WEB_SITE + common.URL_PARAM)
    bingPicUrl = bing2me.getPicUrl(common.WEB_SITE + common.URL_PARAM)
    if bingPicUrl is None:
        print(u'not found picture file')
    else:
        # save picture to disk and setup wallpaper
        print(u'save picture to %s' % common.BING_PIC_DIR)
        print(u'setting wallpaper...')
        bing2me.savePicAndSetWallpaper(bingPicUrl)
        print(u'done')


# 程序开始
main()
