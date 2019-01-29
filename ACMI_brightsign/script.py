'''ACMI BrightSign UDP Node'''

### Libraries required by this Node
import socket
import os

# Gets list of all nodes (but not the ones running on other instances of nodel...)
nodes = os.listdir(os.path.dirname(os.getcwd()))

### Parameters used by this Node. These will be the options available to the user.
param_ipAddress = Parameter({'title': 'IP Address', 'schema': {"type":"string", "required": True}})   
param_port = Parameter({'title': 'Port', 'schema': {"type":"string", "required": True}}) 
param_scheduler = Parameter({'title': 'Scheduler Name', 'schema': 
                             {"type":"string", "required": False, 'enum': nodes},
                             })

#Local actions. Group nodes will call these local_actions when remotely binded to them. These actions
#are the functions that actually 'do something'
@local_action({'group': 'Content', 'title': 'Resume'})
def content_resume(arg = None):
  print 'Action Content:RESUME requested.'
  send_udp_string('RESUME')

@local_action({'group': 'Content', 'title': 'Pause'})
def content_pause(arg = None):
  print 'Action Content:PAUSE requested.'
  send_udp_string('PAUSE')
  
@local_action({'group': 'Audio', 'title': 'Mute'})
def audio_mute(arg = None):
  print 'Action Audio:MUTE requested.'
  send_udp_string('MUTE')

@local_action({'group': 'Audio', 'title': 'Unmute'})
def audio_unmute(arg = None):
  print 'Action Audio:UNMUTE requested.'
  send_udp_string('UNMUTE')

@local_action({'group': 'Audio', 'title': 'Volume up 5%'})
def audio_volume_up(arg = None):
  print 'Action Audio:VOLUP requested.'
  send_udp_string('VOLUP')
  
@local_action({'group': 'Audio', 'title': 'Volume down 5%'})
def audio_volume_down(arg = None):
  print 'Action Audio:VOLDOWN requested.'
  send_udp_string('VOLDOWN')
  
@local_action({'group': 'Display', 'title': 'On'})
def display_on(arg = None):
  print 'Action Display:ON requested.'
  send_udp_string('ON')
  
@local_action({'group': 'Display', 'title': 'Off'})
def display_off(arg = None):
  print 'Action Display:OFF requested.'
  send_udp_string('OFF')

@local_action({'group': 'Power', 'title': 'Reboot'})
def power_reboot(arg = None):
  print 'Action Audio:REBOOT requested.'
  send_udp_string('REBOOT')
  
@local_action({'group': 'Status', 'title': 'Get Status'})
def get_status(arg = None):
  print 'Action Status:get_status requested.'
  get_status()
  
#[0] = group, [1] = action, [2] = event/signal/action name, [3] = handler function for action
action_events_list = [('Power', 'reboot', 'power_reboot', power_reboot),
                      ('Audio', 'mute', 'audio_mute', audio_mute),
                      ('Audio', 'unmute', 'audio_unmute', audio_unmute),
                      ('Audio', 'volume_up', 'audio_volume_up', audio_volume_up),
                      ('Audio', 'volume_down', 'audio_volume_down', audio_volume_down),
                      ('Display', 'on', 'display_on', display_on),
                      ('Display', 'off', 'display_off', display_off),
                      ('Content', 'resume', 'content_resume', content_resume),
                      ('Content', 'pause', 'content_pause', content_pause),
                      ('Status', '', 'get_status', get_status),]


### Functions used by this Node to perform whatever tasks it needs to do.
# This function initialises all the local actions, and remote events that potentially tie a scheduler node
# to this node.
def init_scheduler():
    for action in action_events_list:
        if(lookup_parameter('scheduler') != None):
            remote_name = action[2]
            remote_title = os.path.basename(os.getcwd()) + "_" + remote_name
            remote_metadata = {'Group': action[0], 'title': remote_title}
            print 'Creating remote event: ' + remote_title + ' for: ' + lookup_parameter('scheduler')
            remote_events_list[remote_name].append(remote_title)
            create_remote_event(remote_title , action[3], remote_metadata, lookup_parameter('scheduler'), remote_title)
        else:
            print 'No scheduler specified. Not creating remote scheduler events'


def send_udp_string(msg):
    #open socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if(param_ipAddress != None and param_port != None):
        try:
            config = (str(param_ipAddress), int(param_port))
            print str(config)
            sock.sendto(msg, config)
        except socket.error, msg:
            print "error: %s\n" % msg
            # put this is status 
            #local_event_Error.emit(msg)
        finally:
            if sock:
                sock.close()
    else:
        print 'ipaddress or port empty'
        #report status here
       
# This function builds the status that will be emitted every 60 seconds. If multiple statuses are required,
# this function should aggergate the messages if multple things are wrong with the devices. A case type statement
# should be built and if all statueses are good, the message 'ok' should be returned.
def get_status(arg = None):
    if(param_ipAddress != None):
        ping_response = os.system("ping -n 1 " + param_ipAddress)
    else:
        return {'status_code': '1', 'message': 'No IP Address specified for: ' + os.path.basename(os.getcwd()), 'time': str(date_now())}
    if(ping_response == 0):
        return {'status_code': '0','message': 'ok', 'time': str(date_now())}
    else:
        return {'status_code': '1', 'message': 'Cannot reach ' + os.path.basename(os.getcwd()) + ' with ping at ' + param_ipAddress, 'time': str(date_now())}

### Local events this Node provides. The only event should be the status at ACMI.
# This status will be a message. If all is okay, the status message will be 'ok'.
# If something is wrong, the message will contain what is wrong with the device. 
local_status_name = os.path.basename(os.getcwd()) + '_get_status'

create_local_event(local_status_name, {'Group': 'Status', 'schema': {'title': local_status_name, 'type': 'object', 'properties':{
      'status_code': {'type': 'string'},
      'message': {'type': 'string'},
      'time': {'type': 'string'}
}}})
Timer(lambda: lookup_local_event(local_status_name).emit(get_status()), 60, 1)


### Main
def main(arg = None):
  # Start your script here.
  init_scheduler()
  print 'Node started'
 
