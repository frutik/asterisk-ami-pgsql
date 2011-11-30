#!/usr/bin/env python

from distutils.core import setup

try :
    from AsteriskAmiPGSQL.Version  import VERSION
except :
    VERSION = None

licenses = ( 'Python Software Foundation License'
           , 'GNU Library or Lesser General Public License (LGPL)'
           )

setup \
    ( name = 'AsteriskAmiPGSQL'
    , version = VERSION
    , description = 'A SQL Interface to Asterisk AMI'
    , long_description = ''
    , author = 'Andrew Kornilov'
    , author_email = 'frutik@gmail.com'
    , maintainer = 'Andrew Kornilov'
    , maintainer_email = 'frutik@gmail.com'
    , url = 'https://github.com/frutik/asterisk-ami-pgsql'
    , packages = ['AsteriskAmiPGSQL']
    , license = ', '.join (licenses)
    , platforms = 'Any'
    , classifiers =
        [ 'Development Status :: 5 - Production/Stable'
        , 'Environment :: Other Environment'
        , 'Intended Audience :: Developers'
        , 'Intended Audience :: Telecommunications Industry'
        , 'Operating System :: OS Independent'
        , 'Programming Language :: Python'
        , 'Programming Language :: Python :: 2.4'
        , 'Programming Language :: Python :: 2.5'
        , 'Programming Language :: Python :: 2.6'
        , 'Programming Language :: Python :: 2.7'
        , 'Topic :: Communications :: Internet Phone'
        , 'Topic :: Communications :: Telephony'
        , 'Topic :: Software Development :: Libraries :: Python Modules'
        ] + ['License :: OSI Approved :: ' + l for l in licenses]
    )
