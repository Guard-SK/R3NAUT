from lib.bot import bot
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/London'})

VERSION = "0.1.5." 

bot.run(VERSION)