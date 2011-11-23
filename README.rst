Require

- Postgresql server with installed plpython
- Asterisk server with enabled and configured AMI
- Pyst python module (https://github.com/al-the-x/pyst)

Install
- Download source
- Download, unpack, cd to uncompressed pyst source and install it:
  python setup.py install

- Execute install.sql: psql -U postgres asterisk -f install.sql
- Add your server and required credentials into asterisk.managers table:
  insert into asterisk.managers values ('192.168.1.1', 'me', 'mysecret');

Upgrade
- Download new version
- Execute install script again

Usage

### Call White House's contact center
    asterisk=# select asterisk.originate_async('localhost', 'SIP/117', '92024561111', 'default', 1);
    originate_async 
    -----------------
    t
    (1 row)

### Show 3 online peers
    asterisk=# select * from asterisk.sippeers('localhost') where "IPport" <> '0' limit 3;
    ipport |   status   | chanobjecttype | natsupport | objectname | realtimedevice | dynamic | acl | videosupport | channeltype |   ipaddress    |   event   
    --------+------------+----------------+------------+------------+----------------+---------+-----+--------------+-------------+----------------+-----------
    5060   | OK (5 ms)  | peer           | yes        | 216        | no             | yes     | no  | no           | SIP         | 10.1.10.4      | PeerEntry
    2254   | OK (12 ms) | peer           | yes        | 215        | no             | yes     | no  | no           | SIP         | 10.1.10.3      | PeerEntry
    2253   | OK (12 ms) | peer           | yes        | 214        | no             | yes     | no  | no           | SIP         | 10.1.10.3      | PeerEntry
    (3 rows)

### Check peer

    asterisk=# select "Address-Port", "Status", "CodecOrder", "SIP-Useragent", "MaxCallBR", "Busy-level" from asterisk.sipshowpeer('127.0.0.1', '1117');
     Address-Port |   Status    |     CodecOrder     | SIP-Useragent | MaxCallBR | Busy-level 
    --------------+-------------+--------------------+---------------+-----------+------------
     5060         | OK (234 ms) | ulaw,alaw,g729,gsm | NetDial       | 384 kbps  | 
    (1 row)

### Add agent to queue

    select asterisk.queue_add('localhost', 'incomming_queue', 'AGENT/007');

### Remove agent from queue

    select asterisk.queue_remove('localhost', 'incomming_queue', 'AGENT/007');