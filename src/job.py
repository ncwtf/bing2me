from apscheduler.schedulers.blocking import BlockingScheduler
import util
import common

# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(
    util.change_wallpaper(),
    'cron',
    hour=common.JOB_HOUR,
    minute=common.JOB_MINUTE
)
scheduler.start()
