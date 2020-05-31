loganom
=======

.. image:: https://travis-ci.org/dbaio/loganom.svg?branch=master
    :target: https://travis-ci.org/dbaio/loganom

.. image:: https://readthedocs.org/projects/loganom/badge/?version=latest
    :target: https://loganom.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

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

Sources are available on `<https://github.com/dbaio/loganom>`_.

Documentation available on `<https://loganom.readthedocs.io/en/latest/>`_.

