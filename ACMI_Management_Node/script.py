'''A Template for a Management Node'''
import os
param_localActions = Parameter({'title': 'Local Actions', 'order': 1, 'schema': 
	{'type': 'array', 'items': 
		{'type': 'object', 'properties': 
			{
          		'localAction': {'title': 'Local Action', 'type': 'string','required': True, 'order': 1, 'desc': 'Local Action name.'},
          		'localActionGroup': {'title': 'Local Action Group', 'type': 'string','required': False, 'order': 2, 'desc': 'Drop down group Local Action will appear inside (leave blank for no group).'},
			}
        }
	}
})

param_localEvents = Parameter({'title': 'Local Events', 'order': 2, 'desc': 'Local Event to be added to node.', 'schema': 
	{'type': 'array', 'items': 
		{'type': 'object', 'properties': 
			{
          		'localEvent': {'title': 'Local Event', 'type': 'string', 'required': True, 'order': 1, 'desc': 'Local Event name.'},
				'localEventGroup': {'title': 'Local Event Group', 'type': 'string', 'required': False, 'order': 2, 'desc': 'Drop down group Local Event will appear inside (leave blank for no group).'},
			}
        }
	}
})

param_remoteEventsTriggering = Parameter({'title': 'Remote Events Triggering', 'order': 3, 'schema': 
	{'type': 'array', 'items': 
		{'type': 'object', 'properties': 
			{
          		'targetNode': {'title': 'Target Node', 'type': 'string', 'required': True, 'order': 1, 'desc': 'Target node which Remote Event will bind to.'},
				'targetEvent': {'title': 'Target Event', 'type': 'string', 'required': True, 'order': 2, 'desc': 'Target Event which Remote Event will bind to.'},
				'localActionTrigger': {'title': 'Local Action', 'type': 'string', 'required': True, 'order': 3, 'desc': 'Local Action which will be triggered once bound Local Event is emitted.'},
        	}
        }
	}
})
  
param_memberNodes = Parameter({'title': 'Member Nodes', 'order': 4, 'schema': 
	{'type': 'array', 'items': 
		{'type': 'object', 'properties': 
			{
				'memberNode': {'title': 'Member Node', 'type': 'string', 'required': True, 'order': 1, 'desc': 'Node which Remote Events and Remote Actions will bind to.'},
				'remoteActions': {'title': 'Bind Action', 'type': 'array', 'order': 2, 'items': {'type': 'object', 'properties': 
				{
  	            	'targetAction': {'title': 'Target Action', 'type': 'string', 'required': False, 'order': 1, 'desc': 'Target Action which and Remote Action will bind to (This should have the same name as an available Local Action).'},
				}}},
				'remoteEvents': {'title': 'Bind Event', 'type': 'array', 'order': 3, 'items': {'type': 'object', 'properties': 
				{
       	        	'targetEvent': {'title': 'Target Event', 'type': 'string', 'required': False, 'order': 1, 'desc': 'Target Event which Remote Event will bind to. A Local Action with this name will also be created and bound to Remote Event.'},
       	        	'localEventGroup': {'title': 'Local Event Group', 'type': 'string', 'required': False, 'order': 2, 'desc': 'Drop down group created Local Event will appear inside (leave blank for no group).'},
              }}},
			}
		}
	}
})

eventMetadataTemplate = {
	'Group': '', 
  	'schema': 
	{
		'title': '', 
		'type': 'array',
		'items': 
		{
			'type': 'object', 
			'properties': 
			{
				'message': {'type': 'string'},
				'code': {'type': 'integer'},
				'timestamp': {'type': 'string'}
			}
		}
	}
}


remoteActionList = {}
remoteEventList = []
local_status_name = os.path.basename(os.getcwd()) + 'allNodeEvents'

def emitLocalEvent():
	metadata = {'message' : '', 'code': 0, 'timestamp': ''}
	for event in remoteEventList or []:
		if(event != None):
			remoteEvent = lookup_remote_event(event)
			if(remoteEvent != None):
				if(remoteEvent.getArg() != None):
					metadata['message'] += event + ': ' + remoteEvent.getArg().get('message') + ' - '
					metadata['timestamp'] = date_now()
					if(remoteEvent.getArg().get('code') != 0):
						metadata['code'] = remoteEvent.getArg().get('code')
	lookup_local_event(local_status_name).emit(metadata)

def initialiseNodes():
	# Creates local event to aggregate all other events in to.
	metadata = eventMetadataTemplate.copy()
	metadata['schema']['title'] = 'All Node Events'
	create_local_event(local_status_name, metadata)

	# Handles the creation of the local actions
	for action in lookup_parameter('localActions') or []:
		if(action != None):
			# Each local action should call all remote actions with the same name
#			def triggerRemoteActions(arg):
#				for node in lookup_parameter('memberNodes') or []:
#					if(node != None):
#						remoteActionName = node.get('memberNode') + action.get('localAction')
#						for remoteAction in remoteActionList[action.get('localAction')] or []:
#							if(lookup_remote_action(remoteAction) != None):
#								lookup_remote_action(remoteAction).call()
                                
			def remoteActionTriggerHandlerFactory(actionParameter):
				print('calling action handler factory')
				def f(arg=None):
					for node in lookup_parameter('memberNodes') or []:
						if(node != None):
							remoteActionName = node.get('memberNode') + actionParameter.get('localAction')
							for remoteAction in remoteActionList[actionParameter.get('localAction')] or []:
								if(lookup_remote_action(remoteAction) != None):
									lookup_remote_action(remoteAction).call()
				return f
			#create_local_action(action.get('localAction'), triggerRemoteActions, {'Group': action.get('localActionGroup')})
			create_local_action(action.get('localAction'), remoteActionTriggerHandlerFactory(action), {'Group': action.get('localActionGroup')})

	# Handles the creation of the local events
	for event in lookup_parameter('localEvents') or []:
		if(event != None):
			metadata = eventMetadataTemplate.copy()
			metadata['Group'] = event.get('localEventGroup')
			metadata['schema']['title'] = event.get('localEvent')
			create_local_event(event.get('localEvent'), metadata)
            
	for event in lookup_parameter('remoteEventsTriggering') or []:	
		print(str(event))
		if(event != None):
			def remoteTriggerHandlerFactory(eventParameter):
				print('calling handler factory')

				def f(arg=None):
					action = lookup_local_action(eventParameter.get('localActionTrigger'))
					if(action != None):
						print('calling action ' + eventParameter.get('localActionTrigger'))
						action.call()
					else:
						print('Cannot find local action ' + eventParameter.get('targetAction'))
				return f
			create_remote_event(event.get('targetEvent'), remoteTriggerHandlerFactory(event), None, event.get('targetNode'), event.get('targetEvent')) 

            
	# Handles the creation of Remote Actions, Remote Events, and Local Events to bind node to this Management Node.                               
	for node in lookup_parameter('memberNodes') or []:
		if(node != None):
			for remoteAction in node.get('remoteActions') or []:
				if(remoteAction != None):
					create_remote_action(node.get('memberNode')+remoteAction.get('targetAction'), None, node.get('memberNode'), remoteAction.get('targetAction'))
					if(remoteAction.get('targetAction') not in remoteActionList):
						remoteActionList[remoteAction.get('targetAction')] = []
					remoteActionList[remoteAction.get('targetAction')].append(node.get('memberNode')+remoteAction.get('targetAction'))
			for remoteEventParameter in node.get('remoteEvents') or []:
				if(remoteEventParameter != None):
					metadata = eventMetadataTemplate.copy()
					metadata['Group'] = remoteEventParameter.get('localEventGroup')
					metadata['schema']['title'] = remoteEventParameter.get('targetEvent')
                    
					def remoteEventHandlerFactory(eventName):
						def f(arg=None):
							remoteEvent = lookup_remote_event(eventName)
							if(remoteEvent != None):
								handlerMetadata = {'message': remoteEvent.getArg().get('message'),'code': remoteEvent.getArg().get('code'),'timestamp': date_now()}
								lookup_local_event(eventName).emit(handlerMetadata)
							emitLocalEvent()
						return f
                      
					handler_function = remoteEventHandlerFactory(remoteEventParameter.get('targetEvent'))
					create_remote_event(remoteEventParameter.get('targetEvent'), handler_function, metadata , node.get('memberNode'), remoteEventParameter.get('targetEvent')) 
					remoteEventList.append(remoteEventParameter.get('targetEvent'))
					
					create_local_event(remoteEventParameter.get('targetEvent'), metadata)
				else:
					print('Could not find parameter....')

                    
def main(arg=None):
	print('Node Started')
	initialiseNodes()
