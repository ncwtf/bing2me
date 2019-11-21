import os
import sys
import logging

# 获取壁纸网站
WEB_SITE = 'https://cn.bing.com'
URL_PARAM = "/?scope=web&FORM=HDRSC1"
CONTENT_STR = "data-ultra-definition-src=\""

APP_NAME = "bing2me"
SYS_ARGV = sys.argv[0]
FILE_NAME = os.path.basename(SYS_ARGV)
# 本地保存壁纸目录
USER_PATH = os.path.expanduser('~')
APP_PATH = os.path.abspath('.')
APP_RESOURCE_PATH = USER_PATH + "/.%s" % APP_NAME
BING_PIC_DIR = APP_RESOURCE_PATH + "/bing-pic/"
ICONS_DIR = APP_RESOURCE_PATH + "/icons/"

# database path
DATABASE_PATH = APP_RESOURCE_PATH + '/%s.db' % APP_NAME

# ### icon图片 ### #
STATIC_NCWTF_COM = "https://raw.githubusercontent.com/ncwtf/bing2me/master/icons/"

CHECK_MARK_ICO = "checkmark.ico"
PANDA_ICO = "panda.ico"

CHECK_MARK_ICO_PATH = ICONS_DIR + CHECK_MARK_ICO
PANDA_ICO_PATH = ICONS_DIR + PANDA_ICO

# job config
JOB_HOUR = "09"
JOB_MINUTE = "00"

# log config
LOG_DIR = APP_RESOURCE_PATH + "/logs/"
LOG_FILENAME = LOG_DIR + APP_NAME + ".log"
LOG_LEVEL = logging.INFO
LOG_WHEN = 'D'
LOG_BACK_COUNT = 3
LOG_ENCODING = 'utf-8'
LOG_FMT = '%(asctime)s - %(module)s.%(funcName)s [line:%(lineno)d] - %(levelname)s: %(message)s'
