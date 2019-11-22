import logging
from logging import handlers
import common
import os


class Logger(object):
    def __init__(self):
        self.logger = logging.getLogger(common.LOG_FILENAME)
        if self.logger.handlers:
            return
        if not os.path.exists(common.LOG_DIR):
            os.makedirs(common.LOG_DIR)
        # 设置日志格式
        format_str = logging.Formatter(common.LOG_FMT)
        # 设置日志级别
        self.logger.setLevel(common.LOG_LEVEL)
        # 往屏幕上输出
        sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        sh.setFormatter(format_str)
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(
            filename=common.LOG_FILENAME,
            when=common.LOG_WHEN,
            backupCount=common.LOG_BACK_COUNT,
            encoding=common.LOG_ENCODING
        )
        # 设置文件里写入的格式
        th.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

    def logo(self):
        self.logger.info('''
                                             _                          
             /'                           _-~ `\                        
           /'                            (      )                       
         /'__     O  ,____     ____          _/~   ,__________     ____ 
       /'    )  /'  /'    )  /'    )      _/~     /'    )     )  /'    )
     /'    /' /'  /'    /' /'    /'    _/~      /'    /'    /' /(___,/' 
    (___,/(__(__/'    /(__(___,/(__  /~____,/ /'    /'    /(__(________ 
                             /'                                         
                     /     /'                                           
                    (___,/'                                                                                      
        ''')


LOG = Logger()
LOGGER = LOG.logger
