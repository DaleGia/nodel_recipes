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
remote_actions_list['audio_mute'] = []
remote_actions_list['audio_unmute'] = []
remote_actions_list['audio_volume_up'] = []
remote_actions_list['audio_volume_down'] = []
remote_actions_list['display_on'] = []
remote_actions_list['display_off'] = []
remote_actions_list['content_pause'] = []
remote_actions_list['content_resume'] = []
remote_actions_list['power_reboot'] = []
remote_actions_list['power_on'] = []
remote_actions_list['power_off'] = []
remote_actions_list['lighting_intensity_up'] = []
remote_actions_list['lighting_intensity_down'] = []
remote_actions_list['get_status'] = []
remote_actions_list['all_on'] = []
remote_actions_list['all_off'] = []

remote_events_list = {}
remote_events_list['audio_mute'] = []
remote_events_list['audio_unmute'] = []
remote_events_list['audio_volume_up'] = []
remote_events_list['audio_volume_down'] = []
remote_events_list['display_on'] = []
remote_events_list['display_off'] = []
remote_events_list['content_pause'] = []
remote_events_list['content_resume'] = []
remote_events_list['power_reboot'] = []
remote_events_list['power_on'] = []
remote_events_list['power_off'] = []
remote_events_list['lighting_intensity_up'] = []
remote_events_list['lighting_intensity_down'] = []
remote_events_list['get_status'] = []
remote_events_list['all_on'] = []
remote_events_list['all_off'] = []

local_events_list = {}
local_events_list['audio_mute'] = []
local_events_list['audio_unmute'] = []
local_events_list['audio_volume_up'] = []
local_events_list['audio_volume_down'] = []
local_events_list['display_on'] = []
local_events_list['display_off'] = []
local_events_list['content_pause'] = []
local_events_list['content_resume'] = []
local_events_list['power_reboot'] = []
local_events_list['power_on'] = []
local_events_list['power_off'] = []
local_events_list['lighting_intensity_up'] = []
local_events_list['lighting_intensity_down'] = []
local_events_list['get_status'] = []
local_events_list['all_on'] = []
local_events_list['all_off'] = []

#local_events_list = remote_actions_list.copy()
remote_events_list = remote_actions_list.copy()

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
                                         'volume_up': {'type': 'boolean', 'order': 3, 'title': 'volume_up'},
                                         'volume_down': {'type': 'boolean', 'order': 3, 'title': 'volume_down'},
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
                                           {'intensity_up': {'type': 'boolean', 'order': 1, 'title': 'intensity_up'},
                                            'intensity_down': {'type': 'boolean', 'order': 1, 'title': 'intensity_down'},
                                           }},
                              'Status': {'title': 'Status', 'type': 'object', 'order': 7, 'properties': 
                                         {'get_status': {'type': 'boolean', 'order': 1, 'title': 'status'},
                                         }},
                             }}}})

# These are all the functions that are tied to local actions. They are also based on an ACMI standard and
# should not be deleted. If one of these functions is not required, it should simply print a message in
# in console saying as such.

def call_remote_action(simple_name_action):
   if(lookup_remote_action(simple_name_action) != None):
       print str(simple_name_action)
       lookup_remote_action(simple_name_action).call()
        
#@local_action({'title': 'all_on'})
def all_on(arg = None):
    print 'Action all_on requested.'
    display_on()
    audio_unmute()
    power_on()
    
#@local_action({'title': 'all_off'})
def all_off(arg = None):
    print 'Action all_on requested.'
    display_off()
    audio_mute()
    power_off()    
    
#@local_action({'Display': 'display_on'})
def display_on(arg = None):
    print 'Action Display:on requested.'
    for remote_action in remote_actions_list['display_on']:
        call_remote_action(remote_action)

#@local_action({'Display': 'display_off'})        
def display_off(arg = None):
    print 'Action Display:off requested.'
    for remote_action in remote_actions_list['display_off']:
        call_remote_action(remote_action)

        
#@local_action({'Content': 'content_pause'})
def content_pause(arg = None):
    print 'Action Content:pause requested.'
    for remote_action in remote_actions_list['content_pause']:
        call_remote_action(remote_action)

        
#@local_action({'Content': 'content_resume'})        
def content_resume(arg = None):
    print 'Action Content:resume requested.'
    for remote_action in remote_actions_list['content_resume']:
        call_remote_action(remote_action)

        
#@local_action({'Audio': 'audio_mute'})        
def audio_mute(arg = None):
    print 'Action Mute requested.'
    for remote_action in remote_actions_list['audio_mute']:
        call_remote_action(remote_action)

        
def audio_unmute(arg = None):
    print 'Action Unmute requested.'
    for remote_action in remote_actions_list['audio_unmute']:
        call_remote_action(remote_action)

        
def audio_volume_up(arg = None):
    print 'Action volume up 5% requested.'
    for remote_action in remote_actions_list['audio_volume_up']:
        call_remote_action(remote_action)

def audio_volume_down(arg = None):
    print 'Action volume down 5% requested.'
    for remote_action in remote_actions_list['audio_volume_down']:
        call_remote_action(remote_action)

        
def power_reboot(arg = None):
    print 'Action Power:Reboot requested.'
    for remote_action in remote_actions_list['power_reboot']:
        call_remote_action(remote_action)

        
def power_on(arg = None):
    print 'Action Power:On requested.'
    for remote_action in remote_actions_list['power_on']:
        call_remote_action(remote_action)

        
def power_off(arg = None):
    print 'Action Power:Off requested.'
    for remote_action in remote_actions_list['power_off']:
        call_remote_action(remote_action)

        
def lighting_intensity_up(arg = None):
    print 'Action Lighting:intensity_up requested.'
    for remote_action in remote_actions_list['lighting_intensity_up']:
        call_remote_action(remote_action)

        
def lighting_intensity_down(arg = None):
    print 'Action Lighting:intensity_down requested.'
    for remote_action in remote_actions_list['lighting_intensity_down']:
        call_remote_action(remote_action)

        
def get_status(arg = None):
    print 'Event Status:Status requested.'
    message = ''
    status = '0'
    for remote_event in remote_events_list['get_status']:
        print str(remote_event)

        if(lookup_local_event(remote_event).getArg() != None):
            remote_content = {'status_code': lookup_local_event(remote_event).getArg().get('status_code'), 
                              'message': lookup_local_event(remote_event).getArg().get('message'), 
                              'time': lookup_local_event(remote_event).getArg().get('time')}
            lookup_local_event(remote_event).emit(lookup_local_event(remote_event).getArg())

            if(lookup_local_event(remote_event).getArg().get('message') != 'ok'):
                if(message != ''):
                    message += ' && ' 
                message += lookup_local_event(remote_event).getArg().get('message')
                status = '1'
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
action_events_list = [('Power', 'reboot', 'power_reboot', power_reboot),
                      ('Power', 'on', 'power_on', power_on),
                      ('Power', 'off', 'power_off', power_off),
                      ('Audio', 'mute', 'audio_mute', audio_mute),
                      ('Audio', 'unmute', 'audio_unmute', audio_unmute),
                      ('Audio', 'volume_up', 'audio_volume_up', audio_volume_up),
                      ('Audio', 'volume_down', 'audio_volume_down', audio_volume_down),
                      ('Display', 'on', 'display_on', display_on),
                      ('Display', 'off', 'display_off', display_off),
                      ('Content', 'resume', 'content_resume', content_resume),
                      ('Content', 'pause', 'content_pause', content_pause),
                      ('Lighting', 'intensity_up', 'lighting_intensity_up', lighting_intensity_up),
                      ('Lighting', 'intensity_down', 'lighting_intensity_down', lighting_intensity_down),
                      ('Status', '', 'get_status', get_status),
                      ('', '', 'all_on', all_on),
                      ('', '', 'all_off', all_off)]
        

# This creates the local status event. This will aggregate all the member statuses.
local_status_name = os.path.basename(os.getcwd()) + '_get_status'
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
            remote_title = memberInfo.get('name') + "_" + remote_name
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
            remote_title = os.path.basename(os.getcwd()) + "_" + remote_name
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
