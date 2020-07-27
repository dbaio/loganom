Configuration
-------------

config.ini:

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

    # List of email address that can be skipped
    # email_skip =

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
    url = https://your_mm_url
    api_key = XXXXXXXX
    channel = channel
    icon_url = https://your_icon_logo_url
    username = username