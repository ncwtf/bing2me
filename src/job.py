from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import util
import common
import threading


class Timing(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        # BlockingScheduler
        scheduler = BlockingScheduler()
        trigger = CronTrigger(hour=common.JOB_HOUR, minute=common.JOB_MINUTE)
        scheduler.add_job(util.change_wallpaper, trigger)
        print(u'INFO: job.py.Timing() - 定时任务已启动[%s时, %s分]' % (common.JOB_HOUR, common.JOB_MINUTE))
        scheduler.start()
