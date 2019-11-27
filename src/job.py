from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import util
import common
import threading
import log

logger = log.LOGGER


class Timing(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        # BlockingScheduler
        scheduler = BlockingScheduler()
        trigger = CronTrigger(day="*", hour=common.JOB_HOUR, minute=common.JOB_MINUTE)
        scheduler.add_job(util.change_wallpaper, trigger)
        logger.info(u'定时任务已启动[%s时, %s分]' % (common.JOB_HOUR, common.JOB_MINUTE))
        scheduler.start()
