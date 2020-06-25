.. loganom documentation master file, created by
   sphinx-quickstart on Sun May 24 17:42:26 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

See more about in the :doc:`processor` section.

This is an *experimental* program.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   processor
   usage
   config
   changelog
   ideas

* :ref:`search`