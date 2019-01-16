'''Exhibit Node'''


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
   'Video': {'title': 'Video', 'type': 'object', 'order': 5, 'properties': {
       'pause': {'type': 'boolean', 'order': 3, 'title': 'pause'},
       'resume': {'type': 'boolean', 'order': 3, 'title': 'resume'},

   }},
   'Status': {'title': 'Status', 'type': 'object', 'order': 6, 'properties': {
       'status': {'type': 'boolean', 'order': 3, 'title': 'status'},
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
remote_actions_list['video_pause'] = []
remote_actions_list['video_resume'] = []
remote_actions_list['power_reboot'] = []
remote_actions_list['power_on'] = []
remote_actions_list['power_off'] = []

# Initialises the remote events dict list
remote_events_list = {}
remote_events_list['status'] = []


def initMember(memberInfo):
    name = memberInfo['name']
    print("Initialising member...")

    # Check if null just incase something has gone wrong (this has happened before)
    if(memberInfo.get('Power') != None):
        if(memberInfo.get('Power').get('reboot')):
            print("Adding Power:reboot remote action")
            remote_action_title = memberInfo.get('name') + " Power Reboot"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['power_reboot'].append(create_remote_action(remote_action_title , remote_action_metadata, suggestedNode=memberInfo.get('name'), suggestedAction='power_reboot'))
    
    if(memberInfo.get('Power') != None):                 
        if(memberInfo.get('Power').get('on')):
            print("Adding Power:on remote action")
            remote_action_title = memberInfo.get('name') + " Power On"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['power_on'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'power_on'))

    if(memberInfo.get('Power') != None):         
        if(memberInfo.get('Power').get('off')):
            print("Adding Power:off remote action")
            remote_action_title = memberInfo.get('name') + " Power Off"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['power_off'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'power_off'))
    
    if(memberInfo.get('Audio') != None):
        if(memberInfo.get('Audio').get('mute')):
            print("Adding Audio:mute remote action")
            remote_action_title = memberInfo.get('name') + " Audio Mute"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['audio_mute'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_mute'))
    
    if(memberInfo.get('Audio') != None):
        if(memberInfo.get('Audio').get('unmute')):
            print("Adding Audio:unmute remote action")
            remote_action_title = memberInfo.get('name') + " Audio Unmute"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['audio_unmute'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_unmute'))
    
    if(memberInfo.get('Audio') != None):
        if(memberInfo.get('Audio').get('volume')):  
            print("Adding Audio:volume_up remote action")
            remote_action_title = memberInfo.get('name') + " Audio Volume down 5%"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['audio_volume_down'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_volume_up'))
            
            print("Adding Audio:volume_down remote action")
            remote_action_title = memberInfo.get('name') + " Audio Volume up 5%"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['audio_volume_up'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'audio_volume_down'))
    
    if(memberInfo.get('Display') != None):
        if(memberInfo.get('Display').get('on')):
            print("Adding Display:on remote action")
            remote_action_title = memberInfo.get('name') + " Display On"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['display_on'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'display_on'))
    
    if(memberInfo.get('Display') != None):
        if(memberInfo.get('Display').get('off')):
            print("Adding Display:off remote action")
            remote_action_title = memberInfo.get('name') + " Display Off"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['display_off'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'display_off'))
    
    if(memberInfo.get('Video') != None):
        if(memberInfo.get('Video').get('pause')):
            print("Adding Video:pause remote action")
            remote_action_title = memberInfo.get('name') + " Pause"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['video_pause'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'video_pause'))
    
    if(memberInfo.get('Video') != None):
        if(memberInfo.get('Video').get('resume')):
            print("Adding Video:resume remote action")
            remote_action_title = memberInfo.get('name') + " Resume"
            remote_action_metadata = None #{'title': remote_action_title,'group': 'Members\' "%s"' % remote_action_title, 'schema': {'type': 'boolean'}}
            remote_actions_list['video_resume'].append(create_remote_action(remote_action_title , remote_action_metadata, memberInfo.get('name'), 'video_resume'))

    if(memberInfo.get('Status') != None):
        if(memberInfo.get('Status').get('resume')):
            print("Adding Status remote event")
            remote_event_title = memberInfo.get('status') + " Status"
            remote_event_metadata = None #{'title': remote_event_title,'group': 'Members\' "%s"' % remote_event_title, 'schema': {'type': 'boolean'}}
            remote_events_list['status'].append(create_remote_event(remote_event_title , remote_event_metadata, memberInfo.get('name'), 'status'))


def initSignalSupport(name, memberInfo, signalName, states):
    print 'status support not yet implemented'
#    # look up the members structure (assume
#    members = getMembersInfoOrRegister(signalName, name)
#  
#  
#    # establish local signals if haven't done so already
#    signal = lookup_local_event('signalName')
#    if(signal == None):        
#        signal, created_local_signal = initSignal(signalName, mode, states)
#    else:
#        created_local_signal = lookup_local_event('signalName')
#
#    # establish a remote signal to receive status
#    localMemberSignal = Event(name + ": " + signalName, {'title': + name + ": " + signalName, 'group': signalName, 'order': next_seq(), 'schema': {'type': 'string', 'enum': states}})
#            
#    def aggregateMemberStatus():
#        aggregateLevel = 0
#        aggregateMessage = 'OK'
#    
#        
#        for memberName in members:      
#            memberStatus = lookup_local_event('Status') or []
#      
#            memberLevel = memberStatus.get('level')
#            if memberLevel > aggregateLevel:        
#                aggregateLevel = memberLevel
#      
#                memberMessage = memberStatus.get('message')
#                if(memberLevel > 0):
#                    msgs.append(memberName)
#                else:
#                    msgs.append(memberName + ": " + memberMessage)
#          
#      # for composing the aggegate message at the end
#        msgs = []
#        if(len(msgs) > 0):
#            aggregateMessage = ', '.join(msgs)
#            selfStatusSignal.emit({'level': aggregateLevel, 'message': aggregateMessage})
#            memberStatusSignal.addEmitHandler(lambda arg: aggregateMemberStatus())
#  
#    def handleRemoteEvent(arg):
#        memberStatusSignal.emit(arg)

                          
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


### Functions used by this Node
#none


