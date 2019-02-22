'''ACMI Group Node'''


### Libraries required by this Node
from time import time
from random import randint
import os
 
# Gets list of all nodes (but not the ones running on other instances of nodel...)
nodes = os.listdir(os.path.dirname(os.getcwd()))

# Initialises the remote actions, local_events, and remote_events dict list. These will all be stored 
# in these arrays.
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

remote_events_list = remote_actions_list.copy()
local_events_list = remote_actions_list.copy()

# Parameters that appear in the parameter dialog. Others can be addded and taken away.
# Any changes must also be added to the initMeber() function. These are generic ACMI parameters 
# which should cover most things in gallery spaces.
param_scheduler = Parameter({'title': 'Scheduler Name', 'schema': 
                             {"type":"string", "required": False, 'enum': nodes},
                             })

param_members = Parameter({'title': 'Members', 'schema': 
                           {'type': 'array', 'items': 
                            {'type': 'object', 'properties': 
                             {'name': {'title': 'Node', 'type': 'string', 'required': False, 'enum': nodes, 'order': 1},
                              'Power': {'title': 'Power', 'type': 'object', 'order': 2, 'properties': 
                                        {'reboot': {'type': 'boolean', 'order': 1, 'title': 'reboot'},
                                         'on': {'type': 'boolean', 'order': 2, 'title': 'on'},
                                         'off': {'type': 'boolean', 'order': 3, 'title': 'off'},
                                        }},
                              'Audio': {'title': 'Audio', 'type': 'object', 'order': 3, 'properties': 
                                        {'mute': {'type': 'boolean', 'order': 1, 'title': 'mute'},
                                         'unmute': {'type': 'boolean', 'order': 2, 'title': 'unmute'},
                                         'volumeUp': {'type': 'boolean', 'order': 3, 'title': 'volumeUp'},
                                         'volumeDown': {'type': 'boolean', 'order': 3, 'title': 'volumeDown'},
                                        }},
                              'Display': {'title': 'Display', 'type': 'object', 'order': 4, 'properties': 
                                          {'on': {'type': 'boolean', 'order': 1, 'title': 'on'},
                                           'off': {'type': 'boolean', 'order': 2, 'title': 'off'},
                                          }},
                              'Content': {'title': 'Content', 'type': 'object', 'order': 5, 'properties': 
                                          {'pause': {'type': 'boolean', 'order': 1, 'title': 'pause'},
                                           'resume': {'type': 'boolean', 'order': 2, 'title': 'resume'},
                                          }},
                              'Lighting': {'title': 'Lighting', 'type': 'object', 'order': 6, 'properties': 
                                           {'intensityUp': {'type': 'boolean', 'order': 1, 'title': 'intensityUp'},
                                            'intensityDown': {'type': 'boolean', 'order': 1, 'title': 'intensityDown'},
                                           }},
                              'Status': {'title': 'Status', 'type': 'object', 'order': 7, 'properties': 
                                         {'getStatus': {'type': 'boolean', 'order': 1, 'title': 'status'},
                                         }},
                             }}}})

# These are all the functions that are tied to local actions. They are also based on an ACMI standard and
# should not be deleted. If one of these functions is not required, it should simply print a message in
# in console saying as such.

def call_remote_action(simple_name_action):
   if(lookup_remote_action(simple_name_action) != None):
       print str(simple_name_action)
       lookup_remote_action(simple_name_action).call()
        
#@local_action({'title': 'allOn'})
def allOn(arg = None):
    print 'Action all_on requested.'
    displayOn()
    audio_unmute()
    power_on()
    
#@local_action({'title': 'allOff'})
def allOff(arg = None):
    print 'Action all_on requested.'
    display_off()
    audio_mute()
    power_off()    
    
#@local_action({'Display': 'displayOn'})
def displayOn(arg = None):
    print 'Action Display:on requested.'
    for remote_action in remote_actions_list['displayOn']:
        call_remote_action(remote_action)

#@local_action({'Display': 'displayOff'})        
def displayOff(arg = None):
    print 'Action Display:off requested.'
    for remote_action in remote_actions_list['displayOff']:
        call_remote_action(remote_action)

        
#@local_action({'Content': 'contentPause'})
def contentPause(arg = None):
    print 'Action Content:pause requested.'
    for remote_action in remote_actions_list['contentPause']:
        call_remote_action(remote_action)

        
#@local_action({'Content': 'contentResume'})        
def contentResume(arg = None):
    print 'Action Content:resume requested.'
    for remote_action in remote_actions_list['contentResume']:
        call_remote_action(remote_action)

        
#@local_action({'Audio': 'audioMute'})        
def audioMute(arg = None):
    print 'Action Mute requested.'
    for remote_action in remote_actions_list['audioMute']:
        call_remote_action(remote_action)

        
def audioUnmute(arg = None):
    print 'Action Unmute requested.'
    for remote_action in remote_actions_list['audioUnmute']:
        call_remote_action(remote_action)

        
def audioVolumeUp(arg = None):
    print 'Action volume up 5% requested.'
    for remote_action in remote_actions_list['audioVolumeUp']:
        call_remote_action(remote_action)

def audioVolumeDown(arg = None):
    print 'Action volume down 5% requested.'
    for remote_action in remote_actions_list['audioVolumeDown']:
        call_remote_action(remote_action)

        
def powerReboot(arg = None):
    print 'Action Power:Reboot requested.'
    for remote_action in remote_actions_list['powerReboot']:
        call_remote_action(remote_action)

        
def powerOn(arg = None):
    print 'Action Power:On requested.'
    for remote_action in remote_actions_list['powerOn']:
        call_remote_action(remote_action)

        
def powerOff(arg = None):
    print 'Action Power:Off requested.'
    for remote_action in remote_actions_list['powerOff']:
        call_remote_action(remote_action)

        
def lightingIntensityUp(arg = None):
    print 'Action Lighting:intensity_up requested.'
    for remote_action in remote_actions_list['lightingIntensityUp']:
        call_remote_action(remote_action)

        
def lightingIntensityDown(arg = None):
    print 'Action Lighting:intensity_down requested.'
    for remote_action in remote_actions_list['lightingIntensityDown']:
        call_remote_action(remote_action)

        
def getStatus(arg = None):
    print 'Event Status:Status requested.'
    message = ''
    status = '0'
    for remote_event in remote_events_list['getStatus']:
        print str(remote_event)

        if(lookup_remote_event(remote_event).getArg() != None):
            remote_content = {'status_code': lookup_remote_event(remote_event).getArg().get('status_code'), 
                              'message': lookup_remote_event(remote_event).getArg().get('message'), 
                              'time': lookup_remote_event(remote_event).getArg().get('time')}
            
            lookup_local_event(remote_event).emit(remote_content)

            if(lookup_remote_event(remote_event).getArg().get('message') != 'ok'):
                if(message != ''):
                    message += ' && ' 
                message += lookup_remote_event(remote_event).getArg().get('message')
                status = '1'
        else:
            print('Could not find local event ' + remote_event)
            
        if(message != ''):
            aggregate_message = {'status_code': status, 'message': os.path.basename(os.getcwd()) +': ' + message, 'time': str(date_now())}
            lookup_local_event(local_status_name).emit(aggregate_message)
        else:
            aggregate_message = {'status_code': status, 'message': 'ok', 'time': str(date_now())}
            lookup_local_event(local_status_name).emit(aggregate_message)

# This array of tuples creates a naming convention that ties different groups names, action names, and 
# handler functions together. None of these should be deleted. It is possible to add to this list,
# provided the addition is also added to the relavent Parameter(), and a relevant handling function
# is created.

#[0] = group, [1] = action, [2] = event/signal/action name, [3] = handler function for action
action_events_list = [('Power', 'reboot', 'powerReboot', powerReboot),
                      ('Power', 'on', 'powerOn', powerOn),
                      ('Power', 'off', 'powerOff', powerOff),
                      ('Audio', 'mute', 'audioMute', audioMute),
                      ('Audio', 'unmute', 'audioUnmute', audioUnmute),
                      ('Audio', 'volumeUp', 'audioVolumeUp', audioVolumeUp),
                      ('Audio', 'volumeDown', 'audioVolumeDown', audioVolumeDown),
                      ('Display', 'on', 'displayOn', displayOn),
                      ('Display', 'off', 'displayOff', displayOff),
                      ('Content', 'resume', 'contentResume', contentResume),
                      ('Content', 'pause', 'contentPause', contentPause),
                      ('Lighting', 'intensityUp', 'lightingIntensityUp', lightingIntensityUp),
                      ('Lighting', 'intensityDown', 'lightingIntensityDown', lightingIntensityDown),
                      ('Status', '', 'getStatus', getStatus),
                      ('', '', 'allOn', allOn),
                      ('', '', 'allOff', allOff)]
        

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


# This function creates all the required local events, remote events, and remote actions to bind member nodes
# to the local actions and events of this node. It uses the naming conventions to do this. 
def initMember(memberInfo):
    for action_event in action_events_list:
        if(memberInfo.get(action_event[0]) != None):
            remote_name = action_event[2]
            remote_title = memberInfo.get('name') + remote_name
            if(action_event[0] == 'Status'):
                remote_metadata = {'Group': action_event[0], 'schema': {'title': remote_title, 'type': 'array', 'items': {'type': 'object', 'properties': {
                        'status_code': {'type': 'string'},
                        'message': {'type': 'string'},
                        'time': {'type': 'string'}
                        }}}}
                print 'creating local event: ' + remote_title
                #local_events_list[remote_name].append(create_local_event(remote_title, remote_metadata))
                local_events_list[remote_name].append(remote_title)
                create_local_event(remote_title, remote_metadata)

                
                print 'Creating remote event: ' + remote_name + 'for: ' + memberInfo.get('name')
                #remote_events_list[remote_name].append(create_remote_event(remote_title , action_event[3], remote_metadata, memberInfo.get('name'), remote_title))
                remote_events_list[remote_name].append(remote_title)
                create_remote_event(remote_title , action_event[3], remote_metadata, memberInfo.get('name'), remote_title)
             
            elif(memberInfo.get(action_event[0]).get(action_event[1])):
                if(memberInfo.get(action_event[0]) == ''):
                    remote_metadata = {'title': remote_name}
                else:
                    remote_metadata = {'Group': action_event[0], 'title': remote_title}
                
                print 'Creating remote action: ' + remote_title + ' for: ' + memberInfo.get('name')
                #remote_actions_list[remote_name].append(create_remote_action(remote_title , remote_metadata, str(memberInfo.get('name')), str(remote_name)))
                remote_actions_list[remote_name].append(remote_title)
                create_remote_action(remote_title , remote_metadata, str(memberInfo.get('name')), str(remote_name))
            else:
                print memberInfo.get('name') + ': ' + action_event[2] + ' not required...'

# This function initialises all the local actions, and remote events that potentially tie a scheduler node
# to this node.
def init_scheduler_and_local_actions():
    for action in action_events_list:
        if(lookup_parameter('scheduler') != None):
            remote_name = action[2]
            remote_title = os.path.basename(os.getcwd()) + remote_name
            remote_metadata = {'Group': action[0], 'title': remote_title}
            print 'Creating remote event: ' + remote_title + ' for: ' + lookup_parameter('scheduler')
            #remote_events_list[remote_name].append(create_remote_event(remote_title , action[3], remote_metadata, lookup_parameter('scheduler'), remote_title))
            remote_events_list[remote_name].append(remote_title)
            create_remote_event(remote_title , action[3], remote_metadata, lookup_parameter('scheduler'), remote_title)

        else:
            print 'No scheduler specified. Not creating remote scheduler events'
        if(action[0] == ''):
            local_status_name = os.path.basename(os.getcwd()) + 'action[2]'

            create_local_action(action[2], action[3], {'title': action[2]})
        #    Action(action[2], action[3], {'title': action[2]})
        else:
           # Action(action[2], action[3], {'group': action[0], 'title': action[2]})          

            create_local_action(action[2], action[3], {'group': action[0], 'title': action[2]})          
### Main
def main(arg = None):
    # creates local actions and remote actions for scheduler
    init_scheduler_and_local_actions()
    # Initialises each member of this group as per the saved Parameter()s and creates the required
    # remote action and remote event bindings
    for memberInfo in lookup_parameter('members') or []:
        print 'Initialising member: ' + memberInfo.get('name')
        initMember(memberInfo) 
