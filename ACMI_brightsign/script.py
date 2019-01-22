'''BrightSign UDP Node'''

### Libraries required by this Node
import socket
import os
### Parameters used by this Node. These will be the options available to the user.
param_ipAddress = Parameter('{"title":"IP Address","desc":"The IP address","schema":{"type":"string"}}')
PORT = 5000



### Functions used by this Node to perform whatever tasks it needs to do.
def send_udp_string(msg):
  #open socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    sock.sendto(msg, (param_ipAddress, PORT))
  except socket.error, msg:
    print "error: %s\n" % msg
    local_event_Error.emit(msg)
  finally:
    if sock:
      sock.close()



#Local actions. Group nodes will call these local_actions when remotely binded to them. These actions
#are the functions that actually 'do something'
@local_action({'group': 'Video', 'title': 'Resume'})
def display_resume(arg = None):
  print 'Action Video:RESUME requested.'
  send_udp_string('RESUME')

@local_action({'group': 'Video', 'title': 'Pause'})
def display_pause(arg = None):
  print 'Action Video:PAUSE requested.'
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

### Local events this Node provides. The only event should be the status at ACMI.
# This status will be a message. If all is okay, the status message will be 'ok'.
# If something is wrong, the message will contain what is wrong with the device. 
local_status_name = os.path.basename(os.getcwd()) + ' Status'

create_local_event(local_status_name, {'Group': 'Status', 'schema': {'title': 'status', 'type': 'object', 'properties':{
      'status_code': {'type': 'string'},
      'message': {'type': 'string'},
      'time': {'type': 'string'}
}}})
Timer(lambda: lookup_local_event(local_status_name).emit(get_status()), 60, 1)

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


### Main
def main(arg = None):
  # Start your script here.
  print 'Nodel script started.'
 
