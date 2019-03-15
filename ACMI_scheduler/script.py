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

# Gets list of all nodes (but not the ones running on other instances of nodel...)
nodes = os.listdir(os.path.dirname(os.getcwd()))
# Initialises the remote actions dict list
remote_actions_list = {}
remote_actions_list['audioMute'] = []
remote_actions_list['audioUnmute'] = []
remote_actions_list['audioVolumeUp'] = []
remote_actions_list['audioVolumeDown'] = []
remote_actions_list['displayOn'] = []
remote_actions_list['displayOff'] = []
remote_actions_list['contentPause'] = []
remote_actions_list['contentResume'] = []
remote_actions_list['powerReboot'] = []
remote_actions_list['powerOn'] = []
remote_actions_list['powerOff'] = []
remote_actions_list['lightingIntensityUp'] = []
remote_actions_list['lightingIntensityDown'] = []
remote_actions_list['getStatus'] = []
remote_actions_list['allOn'] = []
remote_actions_list['allOff'] = []


local_events_list = remote_actions_list.copy()
remote_events_list = remote_actions_list.copy()


# This array of tuples creates a naming convention that ties different groups names, action names, and 
# handler functions together. None of these should be deleted. It is possible to add to this list,
# provided the addition is also added to the relavent Parameter(), and a relevant handling function
# is created.

#[0] = group, [1] = action, [2] = event/signal/action name, [3] = handler function for action
action_events_list = ['powerReboot',
                      'powerOn',
                      'powerOff',
                      'audioMute',
                      'audioUnmute',
                      'audioVolume_up',
                      'audioVolume_down',
                      'displayOn',
                      'displayOff',
                      'contentResume',
                      'contentPause',
                      'lightingIntensityUp',
                      'lightingIntensityDown',
                      'getStatus',
                      'allOn',
                      'allOff']
### Parameters used by this Node
param_schedule = Parameter({ "title" : "Schedule", "group" : "Schedule", "schema": 
                              { "type": "array", "title": "Schedule", "required": False, "items": 
                                { "type": "object", "required": False, "properties": 
                                  { "cron": { "type": "string", "format": "cron", "required": True, "title": "Cron", "desc": "Format: <minute> <hour> <day> <month> <day of week>", "order": 1}, 
                                    "except": { "type":"array", "required":False, "order": 2, "title":"Except", "items": { "type":"object", "required":False, "properties":{ "date": { "type":"string", "format":"date", "title":"Date", "required":False } } } }, 
                                    "event": { "type": "string", "enum": action_events_list, "required": True, "title": "Event", "order": 4 }, 
                                    "note": { "type": "string", "format": "long", "required": False, "title": "Notes", "desc": "Schedule notes","order": 5 } 
                                  } 
                                } 
                              } 
                            }
                            )
        

# This creates the local status event. This will aggregate all the member statuses.
local_status_name = os.path.basename(os.getcwd()) + 'getStatus'
status_metadata = {'Group': 'Status', 'schema': {'title': local_status_name, 'type': 'array', 'items': {'type': 'object', 'properties': {
  'status_code': {'type': 'string'},
   'message': {'type': 'string'},
   'time': {'type': 'string'}
   }}}}

print 'creating local event... '
print 'Name: ' + local_status_name
print 'Metadata: ' + str(status_metadata)
create_local_event(local_status_name, status_metadata)

logging.basicConfig()
# 10 second grace time on jobs
sched = Scheduler(misfire_grace_time=10)

def init_local_events():
    create_local_event("Errors,  {'title': Errors})
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
          lookup_local_event("Errors").emit('Invalid cron string')
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
