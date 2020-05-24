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


Sample script with **logtail**:

.. code-block:: sh

    logtail /var/log/maillog > /var/log/maillog-loganom

    loganom postfix-sasl \
        -c ~/.loganom-config.ini \
        -l /var/log/maillog-loganom

    RET=$?
    :> /var/log/maillog-loganom
    exit $RET

If you want to execute **loganom** for instance, in every hour, you can use
**logtail** to get just the log lines that weren't processed yet, this will
avoid reprocessing all log.