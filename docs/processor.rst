Processors
==========


Postfix SASL
------------

.. code-block:: sh

    $ loganom postfix-sasl

It checks accounts authentication through postfix sasl.

Usually when an account is compromised, attackers use several machines from
their botnets to send emails (spam/virus/phishing/etc) with that credential.

This can be observed when a user that usually connects from the same country,
suddenly send emails from all around the world.

IP addresses can be ignored, based on a list of name patterns (dns reverse
name) or based on it's ASN, with the config options *pattern_org* and
*pattern_ip*.

Can be also used the option *country_ignore*, which will ignore IP addresses
from these countries.

This processor needs an *ipinfo.io* api token.

See more in :doc:`config` (General section).


Quota High
----------

.. code-block:: sh

    $ loganom quota-high

It checks email accounts that had their email messages rejected because of rate
limit.

Usually used with PolicyD service.

Example of reject message:

::

    Jun 19 09:04:26 mail-server postfix/smtpd[14222]: NOQUEUE:
    reject: RCPT from host[X.X.X.X]: 554 5.7.1 <anotheruser@domain.com>:
    Recipient address rejected: Quota per hour exceeded;
    from=<user@domain.com> to=<anotheruser@domain.com> proto=ESMTP helo=<ABCD-IR123AB>

If the number of these reject messages from the same sender became too high
(default 150), it is considered an anomaly.

The number of rejecting messages and the reject message itself can be
customized, see more in :doc:`usage` section.

