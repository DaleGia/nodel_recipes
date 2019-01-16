'''BrightSign UDP Node'''

### Libraries required by this Node
import socket



### Parameters used by this Node
param_ipAddress = Parameter('{"title":"IP Address","desc":"The IP address","schema":{"type":"string"}}')
PORT = 5000



### Functions used by this Node
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

### Local events this Node provides
#local_event_Error = LocalEvent('{"title":"Error","desc":"Error","group":"General"}')



### Main
def main(arg = None):
  # Start your script here.
  print 'Nodel script started.'
