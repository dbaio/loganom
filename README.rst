loganom
=======

**loganom** is a tool that checks log files in search for anomalies.
Many small and medium companies that have only local users (in the
same country) can use loganom.

The first processor check postfix sasl authentication.

Usually when an account is compromised, attackers use several machines
from their botnets to send emails (spam/virus/phishing/etc) with that
credential.

This can be observed when a user that usually connects from the same
country, suddenly send emails from all around the world.

This is an experimental program.


Installation
------------

Install using pip:

.. code-block:: sh

    pip install loganom

Sources are available at <https://github.com/dbaio/loganom>.


Usage
-----

Command line usage:

.. code-block:: sh

    loganom postfix-sasl -c config.ini -l logfile


Debugging:

.. code-block:: sh

    LOGLEVEL=DEBUG loganom postfix-sasl -c config.ini -l logfile


Sample execution:

.. code-block:: sh

    LOGLEVEL=DEBUG loganom postfix-sasl -c config.ini -l logfile
    DEBUG:	Starting validating configuration file...
    [postfix-sasl]
    DEBUG:	Starting "postfix-sasl"
    DEBUG:	Log file: logfile
    DEBUG:	Start log reading...
    DEBUG:	user@domain - 92.36.X.Y
    DEBUG:	user@domain - 176.63.X.Y
    [...]
    DEBUG:	user@domain - 188.69.X.Y
    DEBUG:	End log reading...
    DEBUG:	Start processing the dictionary...
    DEBUG:	user@domain (6)
    DEBUG:	Start processing email: user@domain
    DEBUG:	  IP: 209.85.218.52 - Reverse: mail-ej1-f52.google.com.
    DEBUG:	    mail-ej1-f52.google.com. skipped by google
    DEBUG:	  IP: 52.125.129.21 - Reverse: unknown
    DEBUG:	Starting new HTTP connection (1): ipinfo.io:80
    DEBUG:	  Contry: US
    DEBUG:	    AS8075 Microsoft Corporation skipped by AS8075
    [...]

    E-mail address: user@domain
      92.36.X.Y - BA - Bihać - unknown - AS9146 BH Telecom d.d. Sarajevo
      176.63.X.Y - HU - Maklár - catv-176-63-195-207.catv.broadband.hu. - AS6830 Liberty Global B.V.
      195.242.X.Y - UA - Chernihiv - unknown - AS34355 Chernigivtelecom LLC
      188.76.X.Y - ES - Collado-Villalba - 119.17.76.188.dynamic.jazztel.es. - AS12479 Orange Espagne SA
      87.116.X.Y - RS - Belgrade - unknown - AS31042 Serbia BroadBand-Srpske Kablovske mreze d.o.o.
      188.69.X.Y - LT - Vilnius - md-188-69-195-171.omni.lt. - AS8764 Telia Lietuva, AB


Configuration:

.. code-block:: ini

    [GENERAL]
    # Check if the ip address can be ignored, based on a list of name patterns
    pattern_ip = amazonaws.com
      google
      .net.br
      .com.br

    # Check if the ip address can be ignored based on it's ASN
    pattern_org = AS8075
      AS36351
    # AS8075   Microsoft Corporation
    # AS36351  SoftLayer Technologies Inc

    # country_ignore can be a list
    country_ignore = BR

    ipinfo_token = XXXXXXXX

    [SMTP]
    enabled = False
    from = your_mail@from
    to = your_mail@to
    host = localhost
    port = 587
    ssl = False
    user = username
    pass = password
    subject = SMTP authentication, anomalies found...

    [MATTERMOST]
    enabled = False
    url =

Ideas
-----

* Use a database

* Send alert to users

* API to block/unblock users

* Read logs in realtime
