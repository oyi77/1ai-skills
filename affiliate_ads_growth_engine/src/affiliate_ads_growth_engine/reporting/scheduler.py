import schedule
import time

class ReportScheduler:
 def __init__(self):
 self.jobs = []

 def add_daily(self, time_str, func):
 self.jobs.append(schedule.every().day.at(time_str).do(func))

 def run(self):
 while True:
 schedule.run_pending()
 time.sleep(1)
