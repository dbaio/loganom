Usage
-----

Command line usage:

.. code-block:: sh

    $ loganom postfix-sasl -c config.ini -l logfile


It's optional executing an external script when an anomaly is found:

.. code-block:: sh

    $ loganom postfix-sasl -c config.ini -l logfile -e /path/script.sh


Debugging:

.. code-block:: sh

    $ LOGLEVEL=DEBUG loganom postfix-sasl -c config.ini -l logfile


Sample execution:

.. code-block:: sh

    $ LOGLEVEL=DEBUG loganom postfix-sasl -c config.ini -l logfile
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


Sample execution script with **logtail** and virtualenv:

.. code-block:: sh

    #!/bin/sh

    LOG_LEVEL="DEBUG"  #DEBUG/INFO
    CONFIG_INI="~/.loganom-config.ini"
    LOG_READ="/var/log/maillog-loganom"
    LOG_OUT="/var/log/loganom.log"

    logtail /var/log/maillog > "$LOG_READ"

    source ~/.venv/loganom/bin/activate

    env LOGLEVEL="$LOG_LEVEL" \
        loganom postfix-sasl \
        -c "$CONFIG_INI" \
        -l "$LOG_READ" > "$LOG_OUT" 2>&1
    RET=$?

    :> "$LOG_READ"

    exit $RET


If you want to execute **loganom** for instance, in every hour, you can use
**logtail** to get just the log lines that weren't processed yet, this will
avoid reprocessing all log.


Command line options:

.. code-block:: sh

    $ loganom --help
    usage: main.py [-h] [-c CONFIG] [-l LOG] [-e EXEC] {postfix-sasl,foo}

    positional arguments:
    {postfix-sasl,foo}

    optional arguments:
    -h, --help              show this help message and exit
    -c CONFIG, --config CONFIG
                            Path for configuration file
    -l LOG, --log LOG       Path for log file
    -e EXEC, --exec EXEC    External script to be executed when an anomaly is
                            found