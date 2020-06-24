loganom
=======

.. image:: https://github.com/dbaio/loganom/workflows/Python%20package/badge.svg
    :target: https://github.com/dbaio/loganom/actions?query=workflow%3A%22Python+package%22
    :alt: Python package Status

.. image:: https://readthedocs.org/projects/loganom/badge/?version=latest
    :target: https://loganom.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badge.fury.io/py/loganom.svg
    :target: https://pypi.org/project/loganom/

**loganom** is a tool that checks mail log files in search for anomalies.

The first processor check postfix sasl authentication.

Usually when an account is compromised, attackers use several machines from
their botnets to send emails (spam/virus/phishing/etc) with that credential.

This can be observed when a user that usually connects from the same country,
suddenly send emails from all around the world.

This is an *experimental* program.

Installation
------------

Install using pip:

.. code-block:: sh

    pip install loganom

Sources are available on `<https://github.com/dbaio/loganom>`_.

Documentation available on `<https://loganom.readthedocs.io/en/latest/>`_.

