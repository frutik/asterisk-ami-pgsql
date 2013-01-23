## What is this

Attempt to provide access to Asterisk's AMI via Postgres/SQL

## Features

- You can have access to the asterisk's ami from any programming languages which supports access to the postgresql.
- You can employ all power of sql language: sorting, filtering by where clauses, grouping, join resulting output 
  of ami commands (like ordinary database tables) with the real tables.
- You can use your Asterisk as source of data for ETL processes. For example, to collect some stats.

# Require

- Postgresql server with installed plpython
- Asterisk server with enabled and configured AMI
- Python and pip package manager
- Pyst python module (https://github.com/al-the-x/pyst)

On CentOS 6.3

- install repo from http://yum.postgresql.org/repopackages.php
- refresh metainfo: yum update
- yum install postgresql92-server postgresql92-plpython


# Installation

- Download latest released version and extract files from archive.
- Inside of extracted folder execute command:

     pip install -r requirements.txt

- Execute install.sql: 
     
     createlang plpythonu -U postgres asterisk  
     psql -U postgres asterisk -f install.sql

- Add your server and required credentials into asterisk.managers table:

     insert into asterisk.managers values ('192.168.1.1', 'me', 'mysecret');

# Upgrade

- Download new version
- Perform install procedure again

# Usage

## Call White House's contact center
    asterisk=# select asterisk.originate_async('localhost', 'SIP/117', '92024561111', 'default', 1);
    originate_async 
    -----------------
    t
    (1 row)

## Show 3 online peers
    asterisk=# select * from asterisk.sippeers('localhost') where "IPport" <> '0' limit 3;
    ipport |   status   | chanobjecttype | natsupport | objectname | realtimedevice | dynamic | acl | videosupport | channeltype |   ipaddress    |   event   
    --------+------------+----------------+------------+------------+----------------+---------+-----+--------------+-------------+----------------+-----------
    5060   | OK (5 ms)  | peer           | yes        | 216        | no             | yes     | no  | no           | SIP         | 10.1.10.4      | PeerEntry
    2254   | OK (12 ms) | peer           | yes        | 215        | no             | yes     | no  | no           | SIP         | 10.1.10.3      | PeerEntry
    2253   | OK (12 ms) | peer           | yes        | 214        | no             | yes     | no  | no           | SIP         | 10.1.10.3      | PeerEntry
    (3 rows)

## Check peer

    asterisk=# select "Address-Port", "Status", "CodecOrder", "SIP-Useragent", "MaxCallBR", "Busy-level" from asterisk.sipshowpeer('127.0.0.1', '1117');
     Address-Port |   Status    |     CodecOrder     | SIP-Useragent | MaxCallBR | Busy-level 
    --------------+-------------+--------------------+---------------+-----------+------------
     5060         | OK (234 ms) | ulaw,alaw,g729,gsm | NetDial       | 384 kbps  | 
    (1 row)

## Add agent to queue

    select asterisk.queue_add('localhost', 'incomming_queue', 'AGENT/007');

## Remove agent from queue

    select asterisk.queue_remove('localhost', 'incomming_queue', 'AGENT/007');
    
## Show queue status

    asterisk=# select * from asterisk.queue_members('localhost', 'test_te') where "Name" = 'SIP/1113';                                                                                         
      Queue  |   Name   | Location | Membership | Penalty | CallsTaken | LastCall | Status | Paused                                                                                                
    ---------+----------+----------+------------+---------+------------+----------+--------+--------                                                                                               
     test_te | SIP/1113 | SIP/1113 | dynamic    | 1       | 0          | 0        | 5      | 0                                                                                                     
    (1 row)                                                                                                                                                                                        

## Check customers waiting in queue

        test=# select * from asterisk.queue_entries('127.0.0.1', 'test_te');
      Queue  | Position |       Channel       | CallerID | CallerIDName | Wait 
    ---------+----------+---------------------+----------+--------------+------
     test_te | 1        | SIP/430913-02c3aef0 | 430913   | 430913       | 69
    (1 row)



## Check general stats of queue

        test=# select * from asterisk.queue_params('127.0.0.1', 'test_te');
      Queue  | Max | Calls | Holdtime | Completed | Abandoned | ServiceLevel | ServicelevelPerf | Weight 
    ---------+-----+-------+----------+-----------+-----------+--------------+------------------+--------
     test_te | 0   | 1     | 65       | 693       | 284       | 60           | 71.6             | 0
    (1 row)

## Join with the real table

You can do this. But examples will be provided later...

## Limitations

- This solution is not for scaling of access to AMI - you still need use some kind of ami proxy.
- This solution "just works for me". This is not best example of python code.
- Keep in mind - some of those commands could be slow.

