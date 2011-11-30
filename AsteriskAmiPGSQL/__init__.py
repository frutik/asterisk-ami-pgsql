ACTION = 'Action'
QUEUE = 'Queue'

def _get_type_fields(plpy, type_name):
    return_type_attributes_plan = plpy.prepare("""SELECT attname FROM pg_attribute WHERE attrelid = (SELECT oid
        FROM pg_class WHERE relname = $1);""", ["text"])

    return_type_attributes = plpy.execute(return_type_attributes_plan, [type_name])

    result = ''
    for r in return_type_attributes:
        result += str(r['attname']) + ','

    return result

def _get_manager(plpy, hostname):
    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])

    manager.event_registry = []

    return manager

def _handle_queue_member(event, manager):
    manager.event_registry.append(event)

def _handle_queue_entry(event, manager):
    manager.event_registry.append(event)

def _handle_queue_parameter(event, manager):
    manager.event_registry.append(event)

def _handle_peerentry(event, manager):
    manager.event_registry.append(event)

def queue_members(plpy, ami_host, queue):
#    manager = _get_manager(plpy, ami_host)
    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [ami_host], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])
    manager.event_registry = []
    manager.register_event('QueueMember', _handle_queue_member)

    manager.send_action({ACTION : 'QueueStatus', QUEUE : queue})

    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'asterisk_queue_member')

    #plpy.error("error")
    #plpy.fatal("fatal")
    #plpy.debug("debug")
    #plpy.notice("notice")

    result = []
    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
            #plpy.notice("FOUND HEADER " + sip_header)
            record[sip_header] = event.get_header(sip_header, None)
        result.append(record)

    return result

def queue_entries(plpy, ami_host, queue):

    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [ami_host], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])
    manager.event_registry = []
    manager.register_event('QueueEntry', _handle_queue_entry)

    manager.send_action({ACTION : 'QueueStatus', QUEUE : queue})
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'asterisk_queue_entry')

    result = []
    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
            record[sip_header] = event.get_header(sip_header, None)
        result.append(record)

    return result

def queue_params(plpy, ami_host, queue):

    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [ami_host], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])
    manager.event_registry = []
    manager.register_event('QueueEntry', _handle_queue_parameter)

    manager.send_action({ACTION : 'QueueStatus', QUEUE : queue})
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'asterisk_queue_parameter')

    plpy.notice(return_type_attributes)
    plpy.notice(manager.event_registry)

    result = []
    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
            plpy.notice(sip_header)
            record[sip_header] = event.get_header(sip_header, None)

        result.append(record)

    return result

def sip_peers(plpy, hostname):
    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])
    manager.event_registry = []
    manager.register_event('PeerEntry', _handle_peerentry)

    manager.sippeers()
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'peer_entry')

    result = []
    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
            record[sip_header] = event.get_header(sip_header, None)
        result.append(record)

    return result

def originate_async(plpy, hostname, channel, exten, context, priority):
    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])

    manager.originate(channel=channel, exten=exten, context=context, priority=priority, async=True)
    manager.logoff()

    return True

def sipshowpeer(plpy, hostname, peer):
    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])

    ami_result = manager.sipshowpeer(peer=peer)
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'peer')

    result = {}
    for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
        result[sip_header] = ami_result.get_header(sip_header, None)

    return result

def queue_add(plpy, hostname, queue, interface):
    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])

    cdict = {'Action':'QueueAdd'}
    cdict['Interface'] = interface
    cdict['Queue'] = queue
    cdict['Penalty'] = 1
    cdict['Paused'] = False

    response = manager.send_action(cdict)
    manager.logoff()

    return True

def queue_remove(plpy, hostname, queue, interface):
    import asterisk.manager

    plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
    r = plpy.execute(plan, [hostname], 1)
    r = r[0]

    manager = asterisk.manager.Manager()
    manager.connect(r['host'])
    manager.login(r['login'], r['passwd'])

    cdict = {'Action':'QueueRemove'}
    cdict['Interface'] = interface
    cdict['Queue'] = queue

    response = manager.send_action(cdict)
    manager.logoff()

    return True
