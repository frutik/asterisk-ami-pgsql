ACTION = 'Action'
QUEUE = 'Queue'

def test(plpy):
    plpy.notice("test")

def _handle_queue_member(event, manager):
    manager.event_registry.append(event)

def queue_members(plpy, ami_host, queue):

    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])
    manager.event_registry = []
    manager.register_event('QueueMember', _handle_queue_member)

    manager.send_action({ACTION : 'QueueStatus', QUEUE : queue})

    manager.sippeers()
    
    manager.logoff()

    return_type_attributes_plan = plpy.prepare("SELECT asterisk.get_type_fields($1, $2);", ["text", "text"])
    return_type_attributes = plpy.execute(return_type_attributes_plan, [hostname, 'asterisk_queue_member'], 1)

    result = []

    #plpy.error("error")
    #plpy.fatal("fatal")
    #plpy.debug("debug")
    #plpy.notice("notice")

    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
            #plpy.notice("FOUND HEADER " + sip_header)
            record[sip_header] = event.get_header(sip_header, None)
        result.append(record)

    return result

def _handle_queue_entry(event, manager):
    manager.event_registry.append(event)

def queue_entries(plpy, ami_host, queue):

    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])
    manager.event_registry = []
    manager.register_event('QueueEntry', _handle_queue_entry)

    manager.send_action({QUEUE : 'QueueStatus', QUEUE : queue})

    manager.sippeers()

    manager.logoff()

    return_type_attributes_plan = plpy.prepare("SELECT asterisk.get_type_fields($1, $2);", ["text", "text"])
    return_type_attributes = plpy.execute(return_type_attributes_plan, [hostname, 'asterisk_queue_member'], 1)

    result = []

    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
            record[sip_header] = event.get_header(sip_header, None)
        result.append(record)

    return result
