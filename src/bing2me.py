#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import common


def getPicUrl(url):
    r = requests.get(url)
    if not r.ok:
        print(u"ERROR: bing2me.py - 请求网址 %s 错误, 错误码: %d" % (url, r.status_code))
    else:
        bing_content = str(r.content)
        index_of = bing_content.find(common.CONTENT_STR)
        if index_of == -1:
            print(u"ERROR: bing2me.py - 未找到图片url")
        else:
            index_of += len(common.CONTENT_STR)
            pic_url = bing_content[index_of:]
            # pic_url = pic_url[: pic_url.index("\"")]
            pic_url = pic_url[: pic_url.index("&rf")]
            return common.WEB_SITE + pic_url
