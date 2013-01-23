-- TODO cache plans
-- TODO cache credentials

BEGIN;

DROP SCHEMA IF EXISTS asterisk CASCADE;
CREATE SCHEMA asterisk;

create table asterisk.managers (
    host varchar(15) not null primary key,
    login varchar(255) not null,
    passwd varchar(255) not null
);

create unique index asterisk_managers_uk on asterisk.managers (host, login);

insert into asterisk.managers values ('localhost', 'me', 'mysecret');

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

CREATE TYPE asterisk.asterisk_queue_entry AS (
  "Queue" text,
  "Position" text,
  "Channel" text,
  "CallerID" text,
  "CallerIDName" text,
  "Wait" text
);

CREATE TYPE asterisk.asterisk_queue_params AS (
  "Queue" text,
  "Max" text,
  "Calls" text,
  "Holdtime" text,
  "Completed" text,
  "Abandoned" text,
  "ServiceLevel" text,
  "ServicelevelPerf" text,
  "Weight" text
);

CREATE OR REPLACE FUNCTION asterisk.sippeers(hostname text) RETURNS SETOF asterisk.peer_entry AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.sip_peers(plpy, hostname)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.sipshowpeer(hostname text, peer varchar) RETURNS asterisk.peer AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.sipshowpeer(plpy, hostname, peer)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.originate_async(hostname text, channel varchar, exten varchar, context varchar, priority int4) RETURNS boolean AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.originate_async(plpy, hostname, channel, exten, context, priority)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_add(hostname text, queue varchar, interface varchar) RETURNS boolean AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.queue_add(plpy, hostname, queue, interface)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_remove(hostname text, queue varchar, interface varchar) RETURNS boolean AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.queue_remove(plpy, hostname, queue, interface)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_members(hostname text, queue text) RETURNS SETOF asterisk.asterisk_queue_member AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.queue_members(plpy, hostname, queue)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_entries(hostname text, queue text) RETURNS SETOF asterisk.asterisk_queue_entry AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.queue_entries(plpy, hostname, queue)
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION asterisk.queue_params(hostname text, queue text) RETURNS SETOF asterisk.asterisk_queue_params AS $$
  import AsteriskAmiPGSQL
  return AsteriskAmiPGSQL.queue_params(plpy, hostname, queue)
$$ LANGUAGE plpythonu;

COMMIT;