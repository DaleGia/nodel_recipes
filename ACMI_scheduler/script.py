'''ACMI Scheduler Node'''

### Based heavily off the AVDS Scheduler node found in the official nodel recipies repository 

### Libraries required by this Node
import logging
import atexit
from apscheduler.scheduler import Scheduler
import re
import itertools
from datetime import date
import os

### Parameters used by this Node
param_schedule = Parameter({ "title" : "Schedule", "group" : "Schedule", "schema": 
                              { "type": "array", "title": "Schedule", "required": False, "items": 
                                { "type": "object", "required": False, "properties": 
                                  { "cron": { "type": "string", "format": "cron", "required": True, "title": "Cron", "desc": "Format: <minute> <hour> <day> <month> <day of week>", "order": 1}, 
                                    "except": { "type":"array", "required":False, "order": 2, "title":"Except", "items": { "type":"object", "required":False, "properties":{ "date": { "type":"string", "format":"date", "title":"Date", "required":False } } } }, 
                                    "event": { "type": "string", "required": True, "title": "Event", "order": 4 }, 
                                    "note": { "type": "string", "format": "long", "required": False, "title": "Notes", "desc": "Schedule notes","order": 5 } 
                                  } 
                                } 
                              } 
                            }
                            )
        
logging.basicConfig()
# 10 second grace time on jobs
sched = Scheduler(misfire_grace_time=10)

def init_local_events():
    status_metadata = {'Group': 'Errors', 'schema': {'title': "Errors", 'type': 'array', 'items': {'type': 'object', 'properties': {
        'message': {'type': 'string'},
        'time': {'type': 'string'}
     }}}}
    create_local_event("Errors", status_metadata)
    if(param_schedule != None):
        for schedule in param_schedule:
            event = str(schedule.get('event'))
            metadata = {'Group': 'Schedule Event', 'title': event}
            if(lookup_local_event(event) == None):
                create_local_event(event, metadata)
def cleanup():
  sched.shutdown()

atexit.register(cleanup)

_split_re  = re.compile("\s+")
_cron_re = re.compile(r"^(?:[0-9-,*/]+\s){4}[0-9-,*/]+$")
_sched_seq = ('minute', 'hour', 'day', 'month', 'day_of_week')

def callevent(event, dateexcept):
  dateexcept = dateexcept.split(",")
  dates = [date(*[int(y) for y in x.split('-')]) for x in dateexcept if x]
  if(not date.today() in dates):
    print 'calling: '+event
    try:
      lookup_local_event(event).emit() 
    except:
      print 'error calling: '+event
      if(lookup_local_event("Errors") != None):
        lookup_local_event("Errors").emit('error calling: '+event)
  else:
    print 'excluding: '+event



### Main
def main():
  # creates local actions and remote actions for scheduler
  init_local_events()
  sched.start()
  if(param_schedule):
    for schedule in param_schedule:
      if not _cron_re.match(schedule['cron']):
        if(lookup_local_event("Errors") != None):
          lookup_local_event("Errors").emit({"message": "Invalid cron string", "time": date_now()})
        print 'Invalid cron string'
      else:
        split = _split_re.split(schedule['cron'])
        cron = dict(itertools.izip(_sched_seq, split))
        event = schedule['event']
        if('except' in schedule):
          dates = ",".join([x['date'] for x in schedule['except'] if 'date' in x])
        else:
          dates = ''
        expr = "sched.add_cron_job(callevent, args=['"+event+"','"+dates+"'], **cron)"
        eval(expr)
  print 'Nodel script started.'
