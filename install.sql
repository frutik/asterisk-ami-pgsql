#TODO cache plans
#TODO cache credentials

CREATE SCHEMA asterisk;

create table asterisk.managers (
    host varchar(15) not null primary key,
    login varchar(255) not null,
    passwd varchar(255) not null
);

create unique index asterisk_managers_uk on asterisk.managers (host, login);

insert into asterisk.managers values ('localhost', 'me', 'mysecret');

DROP TYPE asterisk.peer_entry cascade;
CREATE TYPE asterisk.peer_entry AS (
    "IPport" text,
    "Status" text,
    "ChanObjectType" text,
    "Natsupport" text,
    "ObjectName" text,
    "RealtimeDevice" text,
    "Dynamic" text,
    "ACL" text,
    "VideoSupport" text,
    "Channeltype" text,
    "IPaddress" text,
    "Event" text
);

CREATE OR REPLACE FUNCTION asterisk.sippeers(hostname text) RETURNS SETOF asterisk.peer_entry AS $$
import asterisk.manager

def handle_peerentry(event, manager):
    manager.event_registry.append(event)

plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
r = plpy.execute(plan, [hostname], 1)
r = r[0]

manager = asterisk.manager.Manager()
manager.connect(r['host'])
manager.login(r['login'], r['passwd'])
manager.event_registry = []
manager.register_event('PeerEntry', handle_peerentry)

manager.sippeers()
manager.logoff()

return_type_attributes_plan = plpy.prepare("SELECT asterisk.get_type_fields($1, $2);", ["text", "text"])
return_type_attributes = plpy.execute(return_type_attributes_plan, [hostname, 'peer_entry'], 1)

result = []

for event in manager.event_registry:
    record = {}
    for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
        record[sip_header] = event.get_header(sip_header, None)
    result.append(record)

return result

$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.get_type_fields(hostname text, type_name text) RETURNS text AS $$

return_type_attributes_plan = plpy.prepare("SELECT attname FROM pg_attribute WHERE attrelid = (SELECT oid FROM pg_class WHERE relname = $1);", ["text"])
return_type_attributes = plpy.execute(return_type_attributes_plan, [type_name])

result = ''

for r in return_type_attributes:
    result += str(r['attname']) + ','

return result

$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.originate_async(hostname text, channel varchar, exten varchar, context varchar, priority int4) RETURNS boolean AS $$
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

$$ LANGUAGE plpythonu;

DROP TYPE asterisk.peer cascade;
CREATE TYPE asterisk.peer AS (
    "ChanObjectType" text,
    "ObjectName" text,
    "Maxforwards" text,
    "Address-Port" text,
    "ACL" text,
    "QualifyFreq" text,
    "Default-addr-port" text,
    "RemoteSecretExist" text,
    "Status" text,
    "CodecOrder" text,
    "Call-limit" text,
    "Parkinglot" text,
    "SIP-T.38Support" text,
    "Default-addr-IP" text,
    "Codecs" text,
    "Response" text,
    "SIP-DTMFmode" text,
    "Address-IP" text,
    "SIP-VideoSupport" text,
    "Language" text,
    "LastMsgsSent" text,
    "SIP-TextSupport" text,
    "Channeltype" text,
    "SIP-T.38MaxDtgrm" text,
    "RegExpire" text,
    "SIP-CanReinvite" text,
    "TransferMode" text,
    "SIP-Sess-Expires" text,
    "SIP-T.38EC" text,
    "ActionID" text,
    "Reg-Contact" text,
    "Callerid" text,
    "SIP-Sess-Timers" text,
    "MaxCallBR" text,
    "SIP-UserPhone" text,
    "MOHSuggest" text,
    "SIP-DirectMedia" text,
    "SIP-Forcerport" text,
    "CID-CallingPres" text,
    "VoiceMailbox" text,
    "SIP-AuthInsecure" text,
    "SIP-RTP-Engine" text,
    "SIP-Sess-Refresh" text,
    "SecretExist" text,
    "MD5SecretExist" text,
    "Default-Username" text,
    "Pickupgroup" text,
    "Context" text,
    "Busy-level" text,
    "SIP-Sess-Min" text,
    "ToHost" text,
    "Dynamic" text,
    "SIP-Useragent" text,
    "AMAflags" text,
    "SIP-PromiscRedir" text,
    "Callgroup" text
);

CREATE OR REPLACE FUNCTION asterisk.sipshowpeer(hostname text, peer varchar) RETURNS asterisk.peer AS $$
import asterisk.manager

plan = plpy.prepare("SELECT * FROM asterisk.managers WHERE host = $1", [ "text" ])
r = plpy.execute(plan, [hostname], 1)
r = r[0]

manager = asterisk.manager.Manager()
manager.connect(r['host'])
manager.login(r['login'], r['passwd'])

ami_result = manager.sipshowpeer(peer=peer)
manager.logoff()

return_type_attributes_plan = plpy.prepare("SELECT asterisk.get_type_fields($1, $2);", ["text", "text"])
return_type_attributes = plpy.execute(return_type_attributes_plan, [hostname, 'peer'], 1)

result = {}

for sip_header in return_type_attributes[0]['get_type_fields'].split(','):
    result[sip_header] = ami_result.get_header(sip_header, None)

return result

$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_add(hostname text, queue varchar, interface varchar) RETURNS boolean AS $$
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

$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_remove(hostname text, queue varchar, interface varchar) RETURNS boolean AS $$
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

$$ LANGUAGE plpythonu;


DROP TYPE asterisk.asterisk_queue_member cascade;
CREATE TYPE asterisk.asterisk_queue_member AS (
    "Queue" text,
    "Name" text,
    "Location" text,
    "Membership" text,
    "Penalty" text,
    "CallsTaken" text,
    "LastCall" text,
    "Status" text,
    "Paused" text
);

DROP TYPE asterisk.asterisk_queue_entry cascade;
CREATE TYPE asterisk.asterisk_queue_entry AS (
  "Queue" text,
  "Position" text,
  "Channel" text,
  "CallerID" text,
  "CallerIDName" text,
  "Wait" text
);

CREATE OR REPLACE FUNCTION asterisk.queue_members(hostname text, queue text) RETURNS SETOF asterisk.asterisk_queue_member AS $$
import AsteriskAmiPGSQL

return AsteriskAmiPGSQL.queue_members(plpy, hostname, queue)

$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_entries(hostname text, queue text) RETURNS SETOF asterisk.asterisk_queue_entry AS $$
import AsteriskAmiPGSQL

return AsteriskAmiPGSQL.queue_entries(plpy, hostname, queue)

$$ LANGUAGE plpythonu;


CREATE OR REPLACE FUNCTION asterisk.test() RETURNS boolean AS $$
import AsteriskAmiPGSQL

AsteriskAmiPGSQL.test(plpy)

return True

$$ LANGUAGE plpythonu;

