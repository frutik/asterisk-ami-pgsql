ACTION = 'Action'
QUEUE = 'Queue'

def _get_type_fields(plpy, type_name):
    return_type_attributes_plan = plpy.prepare("""SELECT attname FROM pg_attribute WHERE attrelid = (SELECT oid
        FROM pg_class WHERE relname = $1);""", ["text"])

    type_attributes = plpy.execute(return_type_attributes_plan, [type_name])

    result = []
    for r in type_attributes:
        result.append(r['attname'])

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
    manager = _get_manager(plpy, ami_host)
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
        for sip_header in return_type_attributes:
            record[sip_header] = event.get_header(sip_header, None)
        result.append(record)

    return result

def queue_entries(plpy, ami_host, queue):
    manager = _get_manager(plpy, ami_host)
    manager.register_event('QueueEntry', _handle_queue_entry)
    manager.send_action({ACTION : 'QueueStatus', QUEUE : queue})
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'asterisk_queue_entry')

    result = []
    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes:
            record[sip_header] = event.get_header(sip_header, None)

        result.append(record)

    return result

def queue_params(plpy, ami_host, queue):
    manager = _get_manager(plpy, ami_host)
    manager.register_event('QueueParams', _handle_queue_parameter)
    manager.send_action({ACTION : 'QueueStatus', QUEUE : queue})
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'asterisk_queue_params')

    result = []
    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes:
            record[sip_header] = event.get_header(sip_header, None)

        result.append(record)

    return result

def sip_peers(plpy, ami_host):
    manager = _get_manager(plpy, ami_host)
    manager.register_event('PeerEntry', _handle_peerentry)
    manager.sippeers()
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'peer_entry')

    result = []
    for event in manager.event_registry:
        record = {}
        for sip_header in return_type_attributes:
            record[sip_header] = event.get_header(sip_header, None)

        result.append(record)

    return result

def sipshowpeer(plpy, ami_host, peer):
    manager = _get_manager(plpy, ami_host)
    ami_result = manager.sipshowpeer(peer=peer)
    manager.logoff()

    return_type_attributes = _get_type_fields(plpy,'peer')

    result = {}
    for sip_header in return_type_attributes:
        result[sip_header] = ami_result.get_header(sip_header, None)

    return result

def originate_async(plpy, ami_host, channel, exten, context, priority):
    manager = _get_manager(plpy, ami_host)
    manager.originate(channel=channel, exten=exten, context=context, priority=priority, async=True)
    manager.logoff()

    return True

def queue_add(plpy, ami_host, queue, interface):
    manager = _get_manager(plpy, ami_host)

    cdict = {ACTION:'QueueAdd'}
    cdict['Interface'] = interface
    cdict[QUEUE] = queue
    cdict['Penalty'] = 1
    cdict['Paused'] = False

    response = manager.send_action(cdict)
    manager.logoff()

    return True

def queue_remove(plpy, ami_host, queue, interface):
    manager = _get_manager(plpy, ami_host)

    cdict = {ACTION:'QueueRemove'}
    cdict['Interface'] = interface
    cdict[QUEUE] = queue

    response = manager.send_action(cdict)
    manager.logoff()

    return True
