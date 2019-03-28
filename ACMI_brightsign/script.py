'''ACMI BrightSign UDP Node'''

### Libraries required by this Node
import socket
import os

# Gets list of all nodes (but not the ones running on other instances of nodel...)
nodes = os.listdir(os.path.dirname(os.getcwd()))

### Parameters used by this Node. These will be the options available to the user.
param_ipAddress = Parameter({'title': 'IP Address', 'schema': {"type":"string", "required": True}})   
param_port = Parameter({'title': 'Port', 'schema': {"type":"string", "required": True}}) 

#Local actions. Group nodes will call these local_actions when remotely binded to them. These actions
#are the functions that actually 'do something'
@local_action({'group': 'Content', 'title': 'RESUME'})
def RESUME(arg = None):
  print 'Action Content:RESUME requested.'
  send_udp_string('RESUME')

@local_action({'group': 'Content', 'title': 'PAUSE'})
def PAUSE(arg = None):
  print 'Action Content:PAUSE requested.'
  send_udp_string('PAUSE')
  
@local_action({'group': 'Audio', 'title': 'MUTE'})
def MUTE(arg = None):
  print 'Action Audio:MUTE requested.'
  send_udp_string('MUTE')

@local_action({'group': 'Audio', 'title': 'UNMUTE'})
def UNMUTE(arg = None):
  print 'Action Audio:UNMUTE requested.'
  send_udp_string('UNMUTE')

@local_action({'group': 'Audio', 'title': 'VOLUP'})
def VOLUP(arg = None):
  print 'Action Audio:VOLUP requested.'
  send_udp_string('VOLUP')
  
@local_action({'group': 'Audio', 'title': 'VOLDOWN'})
def VOLDOWN(arg = None):
  print 'Action Audio:VOLDOWN requested.'
  send_udp_string('VOLDOWN')
  
@local_action({'group': 'Display', 'title': 'DISPLAYON'})
def DISPLAYON(arg = None):
  print 'Action Display:ON requested.'
  send_udp_string('ON')
  
@local_action({'group': 'Display', 'title': 'DISPLAYOFF'})
def DISPLAYOFF(arg = None):
  print 'Action Display:OFF requested.'
  send_udp_string('OFF')

@local_action({'group': 'Power', 'title': 'REBOOT'})
def REBOOT(arg = None):
  print 'Action Audio:REBOOT requested.'
  send_udp_string('REBOOT')

### Functions used by this Node to perform whatever tasks it needs to do.

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
def getStatus(arg = None):
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
local_status_name = os.path.basename(os.getcwd()) + 'getStatus'

create_local_event(local_status_name, {'Group': 'Status', 'schema': {'title': local_status_name, 'type': 'object', 'properties':{
      'status_code': {'type': 'string'},
      'message': {'type': 'string'},
      'time': {'type': 'string'}
}}})
Timer(lambda: lookup_local_event(local_status_name).emit(getStatus()), 60, 1)


### Main
def main(arg = None):
  # Start your script here.
  print 'Node started'
 
