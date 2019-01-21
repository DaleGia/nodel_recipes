'''ACMI Group Node'''


### Libraries required by this Node
from time import time
from random import randint

### Main
def main(arg = None):
    # Initialises each member of this group as per the saved Parameter()s
    for memberInfo in lookup_parameter('members') or []:
        initMember(memberInfo)   

# Parameters that appear in the parameter dialog. Others can be addded and taken away.
# Any changes must also be added to the initMeber() function.
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


# Initialises the remote actions dict list
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

# Initialises the remote events dict list
remote_events_list = {}
remote_events_list['status'] = []


local_events_list = {}
local_events_list['status'] = []

def initMember(memberInfo):
    name = memberInfo['name']
    print("Initialising member...")

    # Check if null just incase something has gone wrong (this has happened before)
    if(memberInfo.get('Power') != None):
        if(memberInfo.get('Power').get('reboot')):
            print("Adding Power:reboot remote action")
            remote_action_title = memberInfo.get('name') + " Power Reboot"
            remote_action_metadata = None
            remote_actions_list['power_reboot'].append(create_remote_action(remote_action_title , remote_action_metadata, suggestedNode=memberInfo.get('name'), suggestedAction='power_reboot'))
    
    if(memberInfo.get('Power') != None):                 
        if(memberInfo.get('Power').get('on')):
            print("Adding Power:on remote action")
            remote_action_title = memberInfo.get('name') + " Power On"
            remote_action_metadata = None 
            remote_actions_list['power_on'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'power_on'))

    if(memberInfo.get('Power') != None):         
        if(memberInfo.get('Power').get('off')):
            print("Adding Power:off remote action")
            remote_action_title = memberInfo.get('name') + " Power Off"
            remote_action_metadata = None 
            remote_actions_list['power_off'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'power_off'))
    
    if(memberInfo.get('Audio') != None):
        if(memberInfo.get('Audio').get('mute')):
            print("Adding Audio:mute remote action")
            remote_action_title = memberInfo.get('name') + " Audio Mute"
            remote_action_metadata = None 
            remote_actions_list['audio_mute'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_mute'))
    
    if(memberInfo.get('Audio') != None):
        if(memberInfo.get('Audio').get('unmute')):
            print("Adding Audio:unmute remote action")
            remote_action_title = memberInfo.get('name') + " Audio Unmute"
            remote_action_metadata = None 
            remote_actions_list['audio_unmute'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_unmute'))
    
    if(memberInfo.get('Audio') != None):
        if(memberInfo.get('Audio').get('volume')):  
            print("Adding Audio:volume_up remote action")
            remote_action_title = memberInfo.get('name') + " Audio Volume Down 5%"
            remote_action_metadata = None 
            remote_actions_list['audio_volume_down'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_volume_up'))
            
            print("Adding Audio:volume_down remote action")
            remote_action_title = memberInfo.get('name') + " Audio Volume Up 5%"
            remote_action_metadata = None
            remote_actions_list['audio_volume_up'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_volume_down'))
    
    if(memberInfo.get('Display') != None):
        if(memberInfo.get('Display').get('on')):
            print("Adding Display:on remote action")
            remote_action_title = memberInfo.get('name') + " Display On"
            remote_action_metadata = None 
            remote_actions_list['display_on'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'display_on'))
    
    if(memberInfo.get('Display') != None):
        if(memberInfo.get('Display').get('off')):
            print("Adding Display:off remote action")
            remote_action_title = memberInfo.get('name') + " Display Off"
            remote_action_metadata = None
            remote_actions_list['display_off'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'display_off'))
    
    if(memberInfo.get('Content') != None):
        if(memberInfo.get('Content').get('pause')):
            print("Adding Content:pause remote action")
            remote_action_title = memberInfo.get('name') + " Pause"
            remote_action_metadata = None
            remote_actions_list['content_pause'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'content_pause'))
    
    if(memberInfo.get('Content') != None):
        if(memberInfo.get('Content').get('resume')):
            print("Adding Content:resume remote action")
            remote_action_title = memberInfo.get('name') + " Resume"
            remote_action_metadata = None 
            remote_actions_list['content_resume'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'content_resume'))

    if(memberInfo.get('Lighting') != None):
        if(memberInfo.get('Lighting').get('intensity')):
            print("Adding Lighting:intensity_up remote action")
            remote_action_title = memberInfo.get('name') + " Lighting Intensity Up 5%"
            remote_action_metadata = None 
            remote_actions_list['lighting_intensity_up'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'lighting_intensity_up'))
    
    if(memberInfo.get('Lighting') != None):
        if(memberInfo.get('Lighting').get('intensity')):
            print("Adding Lighting:intensity_down remote action")
            remote_action_title = memberInfo.get('name') + " Lighting Intensity Down 5%"
            remote_action_metadata = None 
            remote_actions_list['lighting_intensity_down'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'lighting_intensity_down'))

            
    if(memberInfo.get('Status') != None):
        if(memberInfo.get('Status').get('status')):
            print("Adding Status remote event")
            remote_event_title = memberInfo.get('name') + " Status" 
            remote_event_metadata = {'Group': 'Status', 'schema': {'title': remote_event_title, 'type': 'array', 'items': {'type': 'object', 'properties': {
   'message': {'type': 'string'},
   'time': {'type': 'string'}
   }}}}
            #local_events_list['status'].append(create_local_event(remote_event_title, remote_event_metadata))
            remote_events_list['status'].append(create_remote_event(remote_event_title , get_status,remote_event_metadata,  memberInfo.get('name'), 'Get Status'))

     
### Local actions this Node provides
@local_action({'group': 'Display', 'title': 'display on'})
def dsiplay_on(arg = None):
    print 'Action Display:on requested.'
    for remote_action in remote_actions_list['display_on']:
        remote_action.call()

@local_action({'group': 'Display', 'title': 'display off'})
def dsiplay_off(arg = None):
    print 'Action Display:off requested.'
    for remote_action in remote_actions_list['display_off']:
        remote_action.call()
    
@local_action({'group': 'Video', 'title': 'pause'})
def display_pause(arg = None):
    print 'Action Video:pause requested.'
    for remote_action in remote_actions_list['video_pause']:
        remote_action.call()

@local_action({'group': 'Video', 'title': 'resume'})
def display_resume(arg = None):
    print 'Action Display:resume requested.'
    for remote_action in remote_actions_list['video_resume']:
        remote_action.call()
    
@local_action({'group': 'Audio', 'title': 'mute'})
def audio_mute(arg = None):
    print 'Action Mute requested.'
    for remote_action in remote_actions_list['audio_mute']:
        remote_action.call()

@local_action({'group': 'Audio', 'title': 'unmute'})
def audio_unmute(arg = None):
    print 'Action Umute requested.'
    for remote_action in remote_actions_list['audio_unmute']:
        remote_action.call()

@local_action({'group': 'Audio', 'title': 'volume up 5%'})
def audio_volume_up(arg = None):
    print 'Action volume up 5% requested.'
    for remote_action in remote_actions_list['audio_volume_up']:
        remote_action.call()
    
@local_action({'group': 'Audio', 'title': 'volume down 5%'})
def audio_volume_down(arg = None):
    print 'Action volume down 5% requested.'
    for remote_action in remote_actions_list['audio_volume_down']:
        remote_action.call()

@local_action({'group': 'Power', 'title': 'Reboot'})
def power_reboot(arg = None):
    print 'Action Power:Reboot requested.'
    for remote_action in remote_actions_list['power_reboot']:
        remote_action.call()
      
@local_action({'group': 'Power', 'title': 'On'})
def power_on(arg = None):
    print 'Action Power:On requested.'
    for remote_action in remote_actions_list['power_on']:
        remote_action.call()
    
@local_action({'group': 'Power', 'title': 'Off'})
def power_off(arg = None):
    print 'Action Power:Off requested.'
    for remote_action in remote_actions_list['power_off']:
        remote_action.call()

@local_action({'group': 'Lighting', 'title': 'intensity up 5%'})
def lighting_intensity_up(arg = None):
    print 'Action Lighting:intensity_up requested.'
    for remote_action in remote_actions_list['lighting_intensity_up']:
        remote_action.call()
        
@local_action({'group': 'Lighting', 'title': 'intensity down 5%'})
def lighting_intensity_down(arg = None):
    print 'Action Lighting:intensity_down requested.'
    for remote_action in remote_actions_list['lighting_intensity_down']:
        remote_action.call()
        
metadata = {'Group': 'Status', 'schema': {'title': 'Group Status', 'type': 'array', 'items': {'type': 'object', 'properties': {
   'message': {'type': 'string'},
   'time': {'type': 'string'}
   }}}}

create_local_event('Group Status', metadata)

def get_status(arg = None):
    print 'Event Status:Status requested.'
    message = ''
    for remote_event in remote_events_list['status']:
        if(remote_event.getArg().get('message') != 'ok'):
            message += 'Error: ' + remote_event.getArg().get('message')
    
    if(message != ''):
        aggregate_message = {'message': message, 'time': str(date_now())}
        lookup_local_event('Group Status').emit(aggregate_message)
    else:
        aggregate_message = {'message': 'ok', 'time': str(date_now())}
        lookup_local_event('Group Status').emit(aggregate_message)
