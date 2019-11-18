import os

# 获取壁纸网站
WEB_SITE = 'https://cn.bing.com'
URL_PARAM = "/?scope=web&FORM=HDRSC1"
CONTENT_STR = "data-ultra-definition-src=\""
# 本地保存壁纸目录
BING_PIC_DIR = os.path.abspath('.') + "/bing-pic/"
ICONS_DIR = os.path.abspath('.') + "/icons/"


# ### icon图片 ### #
STATIC_NCWTF_COM = "https://raw.githubusercontent.com/ncwtf/bing2me/master/icons/"

CHECK_MARK_ICO = "checkmark.ico"
PANDA_ICO = "panda.ico"

CHECK_MARK_ICO_PATH = ICONS_DIR + CHECK_MARK_ICO
PANDA_ICO_PATH = ICONS_DIR + PANDA_ICO