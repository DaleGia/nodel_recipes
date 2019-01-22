# Copyright (c) 2014 Museum Victoria
# This software is released under the MIT license (see license.txt for details)

'''This is a scheduler node'''

import logging
import atexit
from apscheduler.scheduler import Scheduler
import re
import itertools

logging.basicConfig()
# 10 second grace time on jobs
sched = Scheduler(misfire_grace_time=10)

def cleanup():
  sched.shutdown()

atexit.register(cleanup)

_split_re  = re.compile("\s+")
_cron_re = re.compile(r"^(?:[0-9-,*/]+\s){4}[0-9-,*/]$")
_sched_seq = ('minute', 'hour', 'day', 'month', 'day_of_week')

minute = [0, 10, 20, 30, 40, 50] 
hour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

actions = ['audio_mute', 'audio_unmute', 'audio_volume_down', 'audio_volume_up', 'display_off', 'display_on', 'content_pause', 'content_resume', 'power_on', 'power_off', 'power_reboot'] 
param_schedule = Parameter({'title': 'Scheduler', 'schema': {'type': 'array', 'items': {'type': 'object', 'properties': {
   'name': {'title': 'Node', 'required': True, 'type': 'string', 'order': 1},
   'Date': {'title': 'Date', 'type': 'object', 'order': 2, 'properties': {
       'Minute': {'type': 'string', 'required': True, 'enum': minute, 'order': 1},
       'Hour': {'type': 'string', 'required': True, 'enum': hour, 'order': 2},
       'Day': {'type': 'string', 'required': False, 'enum': day, 'order': 3},
       'Month': {'type': 'string', 'required': False, 'enum': month, 'order': 4},
       'Reoccuring': {'type': 'boolean', 'order': 5},
   }},
   'Action': {'title': 'Action', 'required': True, 'type': 'string', 'enum': actions, 'order': 3}
}}}})


def main():
  sched.start()
  if(param_schedule):
    for schedule in param_schedule:
      if not _cron_re.match(schedule['cron']):
        local_event_Error.emit('Invalid cron string')
        print 'Invalid cron string'
      else:
        split = _split_re.split(schedule['cron'])
        cron = dict(itertools.izip(_sched_seq, split))
        event = "local_event_"+schedule['signal']+".emit"
        args = ''
        if 'args' in schedule:
          args = schedule['args']
        expr = "sched.add_cron_job("+event+", args=['"+args+"'], **cron)"
        print 'expr:', expr
        eval(expr)
