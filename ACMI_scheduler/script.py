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

local_event_AllOn = LocalEvent('{ "title" : "All On", "group" : "Input" }')
local_event_AllOff = LocalEvent('{ "title" : "All Off", "group" : "Input" }')
local_event_Error = LocalEvent('{ "title" : "Error", "group" : "General" }')

param_schedule = Parameter('{ "title" : "Schedule", "group" : "Schedule", "schema": { "type": "array", "title": "Schedule", "required": false, "items": { "type": "object", "required": false, "properties": 
                           { "cron": 
                            { "type": "string", "format": "cron", "required": true, "title": "Cron", "desc": "Format: <minute> <hour> <day> <month> <day of week>" }, 
                            "signal": { "type": "string", "required": true, "title": "Signal" }, 
                            "args": { "type": "string", "required": false, "title": "Args" } } } } }')


param_members = Parameter({'title': 'Members', 'schema': {'type': 'array', 'items': {'type': 'object', 'properties': {
   'name': {'title': 'Node', 'type': 'string', 'order': 1},
   'Power': {'title': 'Power', 'type': 'object', 'order': 2, 'properties': {
       'reboot': {'type': 'boolean', 'order': 1, 'title': 'reboot'},
       'on': {'type': 'boolean', 'order': 2, 'title': 'on'},
       'off': {'type': 'boolean', 'order': 3, 'title': 'off'},
   }},
   'Audio': {'title': 'Audio', 'type': 'object', 'order': 3, 'properties': {
       'mute': {'type': 'boolean', 'order': 1, 'title': 'mute'},
       'unmute': {'type': 'boolean', 'order': 2, 'title': 'unmute'},
       'volume': {'type': 'boolean', 'order': 3, 'title': 'volume'},
   }},
   'Display': {'title': 'Display', 'type': 'object', 'order': 4, 'properties': {
       'on': {'type': 'boolean', 'order': 1, 'title': 'on'},
       'off': {'type': 'boolean', 'order': 2, 'title': 'off'},
   }},
   'Content': {'title': 'Content', 'type': 'object', 'order': 5, 'properties': {
       'pause': {'type': 'boolean', 'order': 1, 'title': 'pause'},
       'resume': {'type': 'boolean', 'order': 2, 'title': 'resume'},

   }},
   'Lighting': {'title': 'Lighting', 'type': 'object', 'order': 6, 'properties': {
       'intensity': {'type': 'boolean', 'order': 1, 'title': 'intensity'},
   }},
   'Status': {'title': 'Status', 'type': 'object', 'order': 7, 'properties': {
       'status': {'type': 'boolean', 'order': 1, 'title': 'status'},
   }},
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
